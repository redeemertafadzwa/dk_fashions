from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from store.models import Order, Product, SearchLog

from .emails import send_code_email
from .forms import CodeForm, LoginForm, SignupForm
from .models import EmailCode

User = get_user_model()

PENDING_KEY = "pending_user_id"
PENDING_PURPOSE = "pending_purpose"


def _start_verification(request, user, purpose):
    """Issue + email a fresh code and stash the pending user in the session."""
    code = EmailCode.issue(user, purpose=purpose)
    try:
        send_code_email(user, code.code, purpose=purpose)
    except Exception as exc:  # surfaces mail-config problems in dev
        messages.error(request, f"We couldn't send the email ({exc}). Try resending.")
    request.session[PENDING_KEY] = user.id
    request.session[PENDING_PURPOSE] = purpose


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password1"],
                full_name=form.cleaned_data["full_name"],
                is_verified=False,
            )
            _start_verification(request, user, "signup")
            messages.success(
                request,
                f"We emailed a 6-digit code to {user.email}. Enter it to confirm your account.",
            )
            return redirect("accounts:verify")
    else:
        form = SignupForm()
    return render(request, "accounts/signup.html", {"form": form})


def verify_view(request):
    user_id = request.session.get(PENDING_KEY)
    purpose = request.session.get(PENDING_PURPOSE, "signup")
    if not user_id:
        messages.info(request, "Start by creating an account or logging in.")
        return redirect("accounts:login")

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        form = CodeForm(request.POST)
        if form.is_valid():
            entered = form.cleaned_data["code"]
            record = (
                EmailCode.objects.filter(user=user, purpose=purpose, is_used=False)
                .order_by("-created_at")
                .first()
            )
            if record and record.is_valid and record.code == entered:
                record.is_used = True
                record.save(update_fields=["is_used"])
                user.is_verified = True
                user.save(update_fields=["is_verified"])
                login(request, user, backend="accounts.backends.EmailBackend")
                request.session.pop(PENDING_KEY, None)
                request.session.pop(PENDING_PURPOSE, None)
                messages.success(request, f"Welcome, {user.display_name}! Your email is confirmed.")
                return redirect("accounts:dashboard")
            elif record and record.is_expired:
                messages.error(request, "That code has expired. We can send you a new one.")
            else:
                messages.error(request, "That code doesn't match. Check your email and try again.")
    else:
        form = CodeForm()

    return render(request, "accounts/verify.html", {"form": form, "email": user.email})


def resend_code_view(request):
    user_id = request.session.get(PENDING_KEY)
    purpose = request.session.get(PENDING_PURPOSE, "signup")
    if not user_id:
        return redirect("accounts:login")
    user = get_object_or_404(User, id=user_id)
    _start_verification(request, user, purpose)
    messages.success(request, f"A new code is on its way to {user.email}.")
    return redirect("accounts:verify")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user is None:
                messages.error(request, "Wrong email or password.")
            elif not user.is_verified:
                _start_verification(request, user, "signup")
                messages.info(
                    request,
                    "Your email isn't confirmed yet — we've sent you a fresh code.",
                )
                return redirect("accounts:verify")
            else:
                login(request, user, backend="accounts.backends.EmailBackend")
                messages.success(request, f"Welcome back, {user.display_name}!")
                nxt = request.GET.get("next")
                return redirect(nxt or "accounts:dashboard")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "You've been logged out.")
    return redirect("store:home")


@login_required
def dashboard_view(request):
    since = timezone.now() - timedelta(days=30)

    recent_searches = SearchLog.objects.filter(user=request.user).order_by("-created_at")[:12]

    most_searched = (
        SearchLog.objects.filter(created_at__gte=since)
        .values("query")
        .annotate(n=Count("id"))
        .order_by("-n")[:8]
    )

    most_bought = Product.objects.filter(purchase_count__gt=0).order_by("-purchase_count")[:6]

    my_orders = Order.objects.filter(user=request.user).order_by("-created_at")[:5]

    context = {
        "recent_searches": recent_searches,
        "most_searched": most_searched,
        "most_bought": most_bought,
        "my_orders": my_orders,
    }
    return render(request, "accounts/dashboard.html", context)


@login_required
def manage_users_view(request):
    if not request.user.is_staff:
        messages.error(request, "You need admin access to view that page.")
        return redirect("accounts:dashboard")

    users = User.objects.all().order_by("-date_joined")
    return render(request, "accounts/manage_users.html", {"users": users})


@login_required
def toggle_admin_view(request, user_id):
    """Grant or revoke admin (staff) privileges. Superusers only."""
    if not request.user.is_superuser:
        messages.error(request, "Only a superuser can change admin privileges.")
        return redirect("accounts:dashboard")
    if request.method != "POST":
        return redirect("accounts:manage_users")

    target = get_object_or_404(User, id=user_id)
    if target == request.user:
        messages.error(request, "You can't change your own admin status here.")
        return redirect("accounts:manage_users")

    target.is_staff = not target.is_staff
    target.save(update_fields=["is_staff"])
    state = "granted" if target.is_staff else "revoked"
    messages.success(request, f"Admin privileges {state} for {target.email}.")
    return redirect("accounts:manage_users")
