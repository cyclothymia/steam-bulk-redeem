import steam.monkey as patcher
patcher.patch_minimal

import os
import steam
import json
import pwinput
from steam.client import SteamClient
from steam.steamid import SteamID
import steam.webauth as wa

class b:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKPURP = '\033[95m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

client = SteamClient()

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    user = input(b.OKPURP + "Enter the steam account username: " + b.ENDC)
    pw = pwinput.pwinput(prompt=b.OKPURP + "Enter the steam account password: " + b.ENDC, mask='*')
    session = wa.WebAuth(username=user, password=pw)
    try:
        session.login()
    except wa.CaptchaRequired:
        print(session.captcha_url)
        captcha = input(b.WARNING + "Please follow the captcha url and enter the code: " + b.ENDC)
        session.login(captcha=captcha)
        logged_in = True
    except wa.EmailCodeRequired:
        code = input(b.WARNING + "Please enter the emailed 2FA code: " + b.ENDC)
        session.login(email_code=code)
        logged_in = True
    except wa.TwoFactorCodeRequired:
        code = input(b.WARNING + "Please enter the 2FA code from the Steam app: " + b.ENDC)
        session.login(twofactor_code=code)
        logged_in = True
    
    if logged_in == True:
        print(b.OKGREEN + "Successfully signed in as %s!" % user + b.ENDC)
    else:
        main()
    
    sessionID = session.session.cookies.get_dict()["sessionid"]
    keys = []
    filename = input(b.OKPURP + "Enter the path for the textfile with codes: " + b.ENDC)
    f = open(filename)
    for line in f:
        keys.append(line)
    
    for key in keys:
        r = session.session.post("https://store.steampowered.com/account/ajaxregisterkey/", data={"product_key": key, "sessionid": sessionID})
        blob = json.loads(r.text)

        if blob["success"] == 1:
            for item in blob["purchase_receipt_info"]["line_items"]:
                print(b.OKGREEN + "Successfully redeemed %s" % item["line_item_description"] + b.ENDC)
        else:
            errorCode = blob["purchase_result_details"]
            sErrorMessage = ""
            if errorCode == 14:
                sErrorMessage = "The product code you've entered is not valid. Please double check to see if you've mistyped your key. I, L, and 1 can look alike, as can V and Y, and 0 and O."
                
            elif errorCode == 15:
                sErrorMessage = "The product code you've entered has already been activated by a different Steam account. This code cannot be used again. Please contact the retailer or online seller where the code was purchased for assistance."

            elif errorCode == 53:
                sErrorMessage = 'There have been too many recent activation attempts from this account or Internet address. Please wait and try your product code again later.'

            elif errorCode == 13:
                sErrorMessage = 'Sorry, but this product is not available for purchase in this country. Your product key has not been redeemed.'

            elif errorCode == 9:
                sErrorMessage = 'This Steam account already owns the product(s) contained in this offer. To access them, visit your library in the Steam client.'

            elif errorCode == 24:
                sErrorMessage = "The product code you've entered requires ownership of another product before activation.\n\nIf you are trying to activate an expansion pack or downloadable content, please first activate the original game, then activate this additional content."

            elif errorCode == 36:
                sErrorMessage = 'The product code you have entered requires that you first play this game on the PlayStation®3 system before it can be registered.\n\nPlease:\n\n- Start this game on your PlayStation®3 system\n\n- Link your Steam account to your PlayStation®3 Network account\n\n- Connect to Steam while playing this game on the PlayStation®3 system\n\n- Register this product code through Steam.'

            elif errorCode == 50: 
                sErrorMessage = 'The code you have entered is from a Steam Gift Card or Steam Wallet Code. Browse here: https://store.steampowered.com/account/redeemwalletcode to redeem it.'

            else:
                sErrorMessage = 'An unexpected error has occurred.  Your product code has not been redeemed.  Please wait 30 minutes and try redeeming the code again.  If the problem persists, please contact <a href="https://help.steampowered.com/en/wizard/HelpWithCDKey%22%3ESteam Support</a> for further assistance.';

            print(b.FAIL + "[ Error ]", sErrorMessage + b.ENDC)

main()