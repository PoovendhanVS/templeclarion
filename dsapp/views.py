from http.client import HTTPResponse
from django.shortcuts import render,redirect
from django.db import connection
import json
from django.http import JsonResponse
import uuid
from django.utils import timezone
from twilio.rest import Client

unique_id = uuid.uuid4()

            
# Twilio credentials (move to settings.py in production)
account_sid = "AC6aa8bc13683b0e26d3fae81e300c8b90"
auth_token = "94002ea8095018fcafbc9ab2c9ae019f"
client = Client(account_sid, auth_token)


# Home Page
def login(request):
    res = {}
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        lsusername = data.get("userName")
        lspassword = data.get("passWord")

        print(lsusername, lspassword)
        try:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT * FROM temple.account_creation  WHERE fullname = %s and pwd = %s""",
                [lsusername,lspassword])
                row = cursor.fetchall()
                print(row)
                if len(row)>0:
                    res = {
                        "status": "success",
                        "message": "Authentication successful! Redirecting to master screen..."
                    }
                else:
                    res={
                        "status": "error",
                        "message": "SECURITY ALERT: Invalid username or password. Access denied."
                    }
        except Exception as e:
            res={
                "status": "error",
                "message": str(e)
            }
        return JsonResponse(res)
        # return redirect(login)  # or success page
    print(res.get('status'))
    print({'resStatus':res.get('status')})
    status = res.get('status')
    
    if status == 'success':
        print('ok')
        # return redirect('mainmaster')
    return render(request, 'AccessPage/login.html')
# Register the User Account
def register(request):
    responsemsg = {}
    if request.method == "POST":
        full_name = request.POST.get("fullName")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirmPassword")
        terms = request.POST.get("terms")  # "on" if checked, None otherwise

        # Example validation
        errors = {}

        if not full_name or len(full_name) < 3:
            errors["full_name"] = "Invalid full name"

        if password != confirm_password:
            errors["password"] = "Passwords do not match"

        if not terms:
            errors["terms"] = "You must accept the terms"

        # if errors:
        #     return render(request, "register.html", {
        #         "errors": errors
        #     })
        
        # Success logic
        print(full_name, email, phone)
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO temple.account_creation (
                        uuid,app,creusrid,credate,trnusrid,trndate,fullname,phone,email,pwd,cfmpwd,isagree,actstat)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s);""", 
                    [str(uuid.uuid4()),1,1001,timezone.now(),1001,timezone.now(),full_name,phone,email,password,
                    confirm_password,1 if terms else 0,1])
                responsemsg = {
                    "status": "success",
                    "message": "Account created successfully"
                }
                # account_sid = "AC6aa8bc13683b0e26d3fae81e300c8b90"
                # auth_token = "94002ea8095018fcafbc9ab2c9ae019f"
                # client = Client(account_sid, auth_token)

                body_text = (
                    "Welcome to our coordination portal\n"
                    f"UserName : {full_name}\n"
                    "Password: {password}\n"
                )

                print(body_text)

                # Send SMS
                # client.messages.create(
                #     from_="+12058610059",
                #     to="+91" + phone,
                #     body=body_text
                # )

        except Exception as e:
            responsemsg={
                "status": "error",
                "message": str(e)
            }
        return redirect(login)  # or success page
    print(responsemsg)
    return render(request, "AccessPage/registration.html", {
        "res": responsemsg
    })
# Forget Passwordimport json
from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection
# from twilio.rest import Client

def forgetpwd(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            print(data, "request-data")

            action_type = data.get("type")  # "otp" or "reset"


            if action_type == "otp":
                phone = data.get("phone_number")
                otp = data.get("otp")
                timestamp = data.get("timestamp")

                if not phone or not otp:
                    return JsonResponse({
                        "status": "error",
                        "message": "Phone number and OTP required"
                    }, status=400)

                # account_sid = "AC6aa8bc13683b0e26d3fae81e300c8b90"
                # auth_token = "94002ea8095018fcafbc9ab2c9ae019f"
                # client = Client(account_sid, auth_token)

                body_text = (
                    "வணக்கம் 🙏\n"
                    f"உங்கள் சரிபார்ப்பு குறியீடு (OTP): {otp}\n"
                    "இந்த குறியீட்டை யாரிடமும் பகிர வேண்டாம்.\n"
                    f"{timestamp}"
                )

                print(body_text)

                # Send SMS
                # client.messages.create(
                #     from_="+12058610059",
                #     to="+91" + phone,
                #     body=body_text
                # )

                return JsonResponse({
                    "status": "success",
                    "message": "OTP sent successfully"
                })
            
            elif action_type == "reset":
                phone = data.get("phone_number")
                new_password = data.get("new_password")

                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE temple.accountcreation
                        SET pwd = %s
                        WHERE phone = %s
                        """,
                        [new_password, phone]
                    )

                    if cursor.rowcount == 0:
                        return JsonResponse({
                            "status": "error",
                            "message": "Phone number not found"
                        }, status=404)

                account_sid = "AC6aa8bc13683b0e26d3fae81e300c8b90"
                auth_token = "94002ea8095018fcafbc9ab2c9ae019f"
                client = Client(account_sid, auth_token)

                body_text = (
                    "வணக்கம் 🙏\n"
                    "உங்கள் கடவுச்சொல் வெற்றிகரமாக மாற்றப்பட்டுள்ளது."
                )

                print(body_text)

                # Send SMS
                # client.messages.create(
                #     from_="+12058610059",
                #     to="+91" + phone,
                #     body=body_text
                # )

                return JsonResponse({
                    "status": "success",
                    "message": "Password reset successfully"
                })

            else:
                return JsonResponse({
                    "status": "error",
                    "message": "Invalid request type"
                }, status=400)

        except json.JSONDecodeError:
            return JsonResponse({
                "status": "error",
                "message": "Invalid JSON format"
            }, status=400)

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)

    return render(request, "AccessPage/forgetpwd.html")


# Donnation 
def mainmaster(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))

            # Extract fields
            full_name = data.get("full_name")
            tamil_name = data.get("tamil_name")
            phone_number = data.get("phone_number")
            email = data.get("email")
            gender = data.get("gender")
            door_number = data.get("door_number")
            family_size = data.get("family_size")
            location = data.get("location")
            donation_type = data.get("donation_type")
            donation_amount = data.get("donation_amount")
            donation_for = data.get("donation_for")
            payment_method = data.get("payment_method")
            timestamp = data.get("timestamp")


            temple_name = "நல்லப்பாழி"

            body_text = (
                f"வணக்கம் 🙏\n"
                f"{tamil_name or full_name} அவர்களின் ₹{donation_amount} காணிக்கை\n"
                f"{temple_name} திருக்கோயிலில் பதிவாகியுள்ளது.\n"
                f"இறையருள் எப்போதும் துணை நிற்கட்டும் 🙏\n"
                f"{timestamp}"
            )

            # Send SMS
            # client.messages.create(
            #     from_="+12058610059",
            #     to= phone_number,
            #     body=body_text
            # )

            # Insert into DB
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO temple.donation_details (
                        uuid, app, creusrid, trnusrid,
                        full_name, tamil_name, phone_number, email, gender,
                        door_number, family_size, location,
                        donation_type, donation_amount, donation_for,
                        payment_method, actstat
                    ) VALUES (
                        %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s
                    )
                    """,
                    [
                        str(uuid.uuid4()),1,1001,1001,full_name,tamil_name,phone_number,
                        email,gender,door_number,family_size,location,donation_type,donation_amount,
                        donation_for,payment_method,1
                    ]
                )

            return JsonResponse({
                "status": "success",
                "message": "Donation saved successfully"
            })

        except json.JSONDecodeError:
            return JsonResponse({
                "status": "error",
                "message": "Invalid JSON format"
            }, status=400)

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)

    return render(request, "AccessPage/mainmaster.html")
# Master Hold
def master(request):
    return render(request,'AccessPage/master.html')

def userentry(request):
    return render(request,'AccessPage/userentry.html')

def requestcredential(request):
    return render(request,'AccessPage/requestcredential.html')

def transalate(request):
    return JsonResponse({"result": "success"})

def payreport(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        try:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT * FROM temple.donation_details""")
                row = cursor.fetchall()
                print(row)
                if len(row)>0:
                    res = {
                        "status": "success"
                    }
                else:
                    res={
                        "status": "error"
                    }
        except Exception as e:
            res={
                "status": "error",
                "message": str(e)
            }
    with connection.cursor() as cursor:
        cursor.execute("""SELECT * FROM temple.donation_details""")
        row = cursor.fetchall()
        # print(row)
        donnation_details = {'results':row}
        print(donnation_details)
    return render(request,'AccessPage/overallpaymentreport.html',donnation_details)
    












































































#########################################################################################################
# Create your views here.
def home(request):
    a = 'poovendhan'
    dstemplatedesign = """
    <div class="topbar d-flex justify-content-between align-items-center">
        <h5 class="mb-0">Dashboard</h5>
        <button class="btn btn-sm btn-outline-primary">Logout</button>
    </div>
    """
    if request.method == "POST":
        name = request.POST.get("username")
        print(name)

    return render(request,'index.html',{"name": a,"dashboard_html": dstemplatedesign
        })

def sysdashboard(request):    
    return render(request,'Page/billsys.html')

def createscreen(request):
    if request.method == "POST":
        for key, value in request.POST.items():
            print(f"{key} = {value}")
    data = dict(request.POST)
    print(data)

    return render(request, "Page/design.html")


def show_design(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT design1
            FROM poventure.designlookup
            WHERE serialno = %s
        """, [1])   # serialno = 1 (safe parameter)

        row = cursor.fetchone()
    print(row)
    design_html = row[0] if row else ""

    return render(request, "Page/designview.html", {
        "design_html": design_html
    })

def billing(request):
    return render(request,'Page/billing.html')
