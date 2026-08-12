from django.shortcuts import render
from django.shortcuts import render, redirect
from django.core.mail import send_mail
import random
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import LoanCategory
from django.shortcuts import render,get_object_or_404
from .models import Signup, PasswordResetOTP
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import UserProfile




# Create your views here.
def home(request):
    categories = LoanCategory.objects.filter(is_active=True)

    return render(request,'index.html',
        {
            'categories': categories
        }
    )




# def login_view(request):

#     # LOGIN BUTTON CLICK

#     if request.method == "POST":

#         email = request.POST.get("email")

#         password = request.POST.get("password")

#         try:

#             # CHECK USER

#             user = Signup.objects.get(
#                 email=email,
#                 password=password
#             )

#             # SAVE SESSION

#             request.session["user_id"] = user.id

#             request.session["email"] = user.email

#             # REDIRECT TO DASHBOARD

#             return redirect("dashboard")

#         except Signup.DoesNotExist:

#             return render(
#                 request,
#                 "login.html",
#                 {
#                     "error": "Invalid Email or Password"
#                 }
#             )

#     return render(request, "login.html")



def login_view(request):

    next_url = request.GET.get("next")

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(

            request,

            username=email,

            password=password

        )

        if user:

            login(
                request,
                user
            )

            if next_url:

                return redirect(next_url)

            return redirect("dashboard")

        messages.error(
            request,
            "Invalid email or password"
        )

    return render(
        request,
        "login.html"
    )


def signup(request):

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return render(
                request,
                "signup.html"
            )

        # CHECK EXISTING USER

        from django.contrib.auth.models import User

        if User.objects.filter(username=email).exists():

            messages.error(
                request,
                "Account already exists."
            )

            return render(
                request,
                "signup.html"
            )

        otp = random.randint(100000, 999999)

        # STORE TEMP DATA IN SESSION

        request.session["signup_name"] = full_name
        request.session["signup_mobile"] = mobile
        request.session["signup_email"] = email
        request.session["signup_password"] = password
        request.session["signup_otp"] = str(otp)

        print("\n===================================")
        print("      FINLOAN OTP VERIFICATION     ")
        print("===================================")
        print(f"User Email : {email}")
        print(f"OTP CODE   : {otp}")
        print("===================================\n")

        return redirect("verify_otp")

    return render(request, "signup.html")

# def signup(request):

#     if request.method == "POST":

#         full_name = request.POST.get("full_name")

#         mobile = request.POST.get("mobile")

#         email = request.POST.get("email")

#         password = request.POST.get("password")

#         confirm_password = request.POST.get("confirm_password")

#         # CREATE USER

#         user = Signup.objects.create(
#             full_name=full_name,
#             mobile=mobile,
#             email=email,
#             password=password,
#             confirm_password=confirm_password,
#         )

#         # SAVE EMAIL IN SESSION

#         # request.session["email"] = user.email

#         # # SEND OTP TO EMAIL

#         # send_mail(
#         #     'FinLoan OTP Verification',
#         #     f'Your OTP is {user.otp}',
#         #     'yourgmail@gmail.com',
#         #     [email],
#         #     fail_silently=False,
#         # )

#         request.session["email"] = user.email

#         # ==============================
#         # OTP PRINT IN TERMINAL
#         # ==============================

#         print("\n===================================")
#         print("      FINLOAN OTP VERIFICATION     ")
#         print("===================================")
#         print(f"User Email : {user.email}")
#         print(f"OTP CODE   : {user.otp}")
#         print("===================================\n")

#         return redirect("verify_otp")

#     return render(request, "signup.html")





# def verify_otp(request):

#     if request.method == "POST":

#         entered_otp = request.POST.get("otp")

#         email = request.session.get("email")

#         if not email:
#             return redirect("signup")

#         try:
#             user = Signup.objects.get(email=email)

#         except Signup.DoesNotExist:
#             return redirect("signup")

#         # OTP MATCH

#         if user.otp == entered_otp:

#             return render(request, "verify_otp.html", {
#                 "verified": True
#             })

#         # WRONG OTP

#         return render(request, "verify_otp.html", {
#             "verified": False,
#             "error": "Invalid OTP"
#         })

#     return render(request, "verify_otp.html")



def verify_otp(request):

    if request.method == "POST":

        entered_otp = request.POST.get("otp")

        saved_otp = request.session.get("signup_otp")

        if entered_otp == saved_otp:

            user = User.objects.create_user(

                username=request.session["signup_email"],
                email=request.session["signup_email"],
                password=request.session["signup_password"],
                first_name=request.session["signup_name"]

            )

            UserProfile.objects.create(

                user=user,
                mobile=request.session["signup_mobile"]

            )

            # AUTO LOGIN

            login(request, user)

            # CLEAR TEMP SESSION

            request.session.pop("signup_name", None)
            request.session.pop("signup_mobile", None)
            request.session.pop("signup_email", None)
            request.session.pop("signup_password", None)
            request.session.pop("signup_otp", None)

            return redirect("dashboard")

    return render(
        request,
        "verify_otp.html"
    )

def resend_otp(request):

    email = request.session.get("email")

    if not email:
        return redirect("signup")

    try:
        user = Signup.objects.get(email=email)

    except Signup.DoesNotExist:
        return redirect("signup")

    # GENERATE NEW OTP

    new_otp = str(random.randint(100000, 999999))

    user.otp = new_otp

    user.save()

    # PRINT OTP IN TERMINAL

    print("===================================")
    print("NEW OTP :", new_otp)
    print("===================================")

    return redirect("verify_otp")



# =========================
# DASHBOARD VIEW
# =========================

def dashboard(request):

    # CHECK LOGIN SESSION

    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    try:

        # FETCH LOGGED IN USER

        user = Signup.objects.get(id=user_id)

    except Signup.DoesNotExist:

        return redirect("login")


    # =========================
    # DASHBOARD DYNAMIC DATA
    # =========================

    context = {

        # USER DETAILS

        "user": user,


        # TOP CARDS

        "total_loans": 2,

        "approved_amount": 850000,

        "emi_due": 12450,

        "credit_score": 750,


        # RECOMMENDED LOAN

        "recommended_loan": {

            "loan_type": "Personal Loan",

            "loan_amount": 1000000,

            "interest_rate": "11.49%",

            "tenure": "12 - 60 Months",

            "features": [

                "Quick disbursal",

                "Minimal documentation",

                "Flexible repayment",

            ]

        },


        # LOAN JOURNEY

        "loan_journey": [

            {

                "title": "Apply",

                "status": "completed",

                "description": "Application Submitted"

            },

            {

                "title": "KYC",

                "status": "active",

                "description": "Under Verification"

            },

            {

                "title": "Approval",

                "status": "pending",

                "description": "In Review"

            },

            {

                "title": "Disbursal",

                "status": "pending",

                "description": "Pending"

            },

        ],


        # LOAN CATEGORIES

        "loan_categories": [

            {

                "name": "Personal Loan",

                "icon": "fa-user"

            },

            {

                "name": "Home Loan",

                "icon": "fa-house"

            },

            {

                "name": "Education Loan",

                "icon": "fa-graduation-cap"

            },

            {

                "name": "Business Loan",

                "icon": "fa-briefcase"

            },

            {

                "name": "Gold Loan",

                "icon": "fa-coins"

            },

            {

                "name": "Car Loan",

                "icon": "fa-car"

            },

        ],


        # SIDEBAR MENU

        "sidebar_menu": [

            {

                "name": "Dashboard",

                "icon": "fa-table-columns",

                "url": "/dashboard/"

            },

            {

                "name": "Explore Loans",

                "icon": "fa-compass",

                "url": "#"

            },

            {

                "name": "My Applications",

                "icon": "fa-file-lines",

                "url": "#"

            },

            {

                "name": "My Loans",

                "icon": "fa-wallet",

                "url": "#"

            },

            {

                "name": "Payments",

                "icon": "fa-credit-card",

                "url": "#"

            },

            {

                "name": "Documents",

                "icon": "fa-folder-open",

                "url": "#"

            },

            {

                "name": "Profile",

                "icon": "fa-user",

                "url": "#"

            },

            {

                "name": "Notifications",

                "icon": "fa-bell",

                "url": "#"

            },

            {

                "name": "Support",

                "icon": "fa-headset",

                "url": "#"

            },

        ],


        # NOTIFICATION COUNT

        "notification_count": 3,

    }


    return render(request,"dashboard.html", context)




def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email")

        try:

            user = Signup.objects.get(email=email)

            otp = str(random.randint(100000,999999))

            PasswordResetOTP.objects.create(
                email=email,
                otp=otp
            )

            print("OTP :", otp)
            print("RESET OTP :", otp)

            request.session['reset_email'] = email

            return redirect('verify_reset_otp')

        except Signup.DoesNotExist:

            messages.error(
                request,
                "Email not found."
            )

    return render(
        request,
        'forgot_password.html'
    )

def verify_reset_otp(request):

    email = request.session.get('reset_email')

    if request.method == "POST":

        entered_otp = request.POST.get("otp")

        otp_obj = PasswordResetOTP.objects.filter(
            email=email,
            otp=entered_otp
        ).last()

        if otp_obj:

            request.session['otp_verified'] = True

            return redirect('reset_password')

        else:

            messages.error(
                request,
                "Invalid OTP"
            )

    return render(
        request,
        'verify_reset_otp.html'
    )


def reset_password(request):

    if not request.session.get('otp_verified'):
        return redirect('forgot_password')

    email = request.session.get('reset_email')

    if request.method == "POST":

        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return redirect('reset_password')

        try:

            user = Signup.objects.get(email=email)

            user.password = password
            user.confirm_password = password

            user.save()

            request.session.flush()

            messages.success(
                request,
                "Password updated successfully."
            )

            return redirect('reset_success')

        except Signup.DoesNotExist:

            messages.error(
                request,
                "User not found."
            )

            return redirect('forgot_password')

    return render(
        request,
        'reset_password.html'
    )

def resend_reset_otp(request):

    email = request.session.get('reset_email')

    if not email:
        return redirect('forgot_password')

    otp = str(random.randint(100000,999999))

    PasswordResetOTP.objects.create(
        email=email,
        otp=otp
    )

    print("RESET OTP :", otp)

    return redirect('verify_reset_otp')

def reset_success(request):

    return render(request,'reset_success.html' )


def how_it_works(request):

    return render(request,'how_it_works.html')

def features(request):
    return render(request, 'features.html')

def about(request):
    return render(request, 'about.html')


def loan_detail(request,id):

    loan = get_object_or_404(
        LoanCategory,
        id=id,
        is_active=True
    )

    return render(request,'loan_detail.html',
        {
            'loan':loan
        }
    )



def check_eligibility(request):

    if request.method == "POST":

        age = request.POST.get("age")
        income = request.POST.get("income")

        # Guest User
        if not request.session.get("user_id"):

            request.session["guest_eligibility"] = {
                "age": age,
                "income": income,
            }

        # Logged In User
        else:

            user_id = request.session["user_id"]

            # Save in database
            # EligibilityData.objects.create(...)

        return redirect("eligibility_result")

    return render(
        request,
        "check_eligibility.html"
    )

def logout_view(request):

    # CLEAR SESSION

    request.session.flush()

    # SUCCESS MESSAGE

    messages.success(request, "Logged out successfully." )

    # REDIRECT TO LOGIN PAGE

    return redirect("login")