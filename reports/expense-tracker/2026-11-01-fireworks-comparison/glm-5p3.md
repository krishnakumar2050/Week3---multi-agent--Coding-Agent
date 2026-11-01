# Code review report

Status: **complete**

Static test-gap analysis only; tests were not executed and coverage was not measured.

critical: 0 | high: 10 | medium: 10 | low: 5 | info: 1

## Aggregator synthesis

3/3 specialists succeeded; 26 verified finding(s). Highest reported severity: high.

- [HIGH] `Expense Tracker/Controllers/Login SingUp/LoginWithPinVC.swift:177` Account access via 4-digit PIN with no rate limiting or lockout: Enforce server-side rate limiting, attempt counters, and temporary lockout on the PIN endpoint; require a second factor (e.g., username) with the PIN; and add client-side attempt throttling. A 4-digit sole credential is too weak for account-level authentication.
- [HIGH] `Expense Tracker/Controllers/Login SingUp/SingUpVC.swift:165` Force unwrap crash on invalid PIN during sign-up: Use optional binding for the pin and show an invalid-PIN alert on failure; reject non-4-digit pins before networking.
- [HIGH] `Expense Tracker/Controllers/Login SingUp/SingUpVC.swift:165` Force unwrap of non-numeric PIN crashes sign-up: Use `guard let pin = Int(pinTextFeild.text ?? "") else { present validation error; return }` and set keyboardType = .numberPad on the PIN field.
- [HIGH] `Expense Tracker/Controllers/Login SingUp/SingUpVC.swift:185` 4-character limit applied to every signup field via shared UITextFieldDelegate: Apply the 4-char limit only to pinTextFeild (e.g., `if textField === pinTextFeild`).
- [HIGH] `Expense Tracker/Controllers/Main/AddIncomeAndExpensesVC.swift:237` Force unwrap crash on non-numeric amount in postTransaction: Replace the force unwrap with optional binding (e.g., `guard let amount = Double(text)` else present an alert) and remove the "$0" seed text or strip "$` before conversion.

Run: `fed5b224-b681-4d6f-8506-cd9fb8378727` · Schema: 1.0

Repository: `/Users/krishnakumar/Documents/GitHub/Expense-Tracker-App`

Snapshot SHA-256: `83ab6449ed7aab7c754f304211b83cc5e8bb9d96ec92f5933d5d63953883c24d`

Completed: 2026-11-01T10:20:01.777479+00:00 · Duration: 37.049 seconds

## Model provenance

| Agent | Requested model | Actual model | Evidence |
| --- | --- | --- | --- |
| quality | accounts/fireworks/models/glm-5p3 | accounts/fireworks/models/glm-5p3 | provider_response |
| security | accounts/fireworks/models/glm-5p3 | accounts/fireworks/models/glm-5p3 | provider_response |
| tests | accounts/fireworks/models/glm-5p3 | accounts/fireworks/models/glm-5p3 | provider_response |

## 1. [HIGH] Account access via 4-digit PIN with no rate limiting or lockout

Location: `Expense Tracker/Controllers/Login SingUp/LoginWithPinVC.swift:177` · Agents: security

LoginWithPinVC allows full account access by submitting only a 4-digit numeric PIN (10,000 combinations) constructed from four single-character fields (line 170). The client-side guard only checks non-emptiness. There is no visible rate limiting, attempt counting, backoff, or lockout anywhere in the snapshot, so an attacker with a stolen device or network position can brute-force the PIN space (or any user's PIN) and receive a full access token (AuthManager.login(with:) stores access_token on success).

Fix: Enforce server-side rate limiting, attempt counters, and temporary lockout on the PIN endpoint; require a second factor (e.g., username) with the PIN; and add client-side attempt throttling. A 4-digit sole credential is too weak for account-level authentication.

Suggested test: Automate 10,000 sequential PIN submissions against the auth/pin endpoint in a test environment; assert the server rejects requests after N failed attempts (e.g., 5) with an HTTP 429 or lockout response instead of eventually returning 200.

Evidence:

````
                        let result = try await AuthManager.shared.login(with: pin)
````

## 2. [HIGH] Force unwrap crash on invalid PIN during sign-up

Location: `Expense Tracker/Controllers/Login SingUp/SingUpVC.swift:165` · Agents: tests

Int(pinTextFeild.text!)! crashes when the PIN field contains a non-numeric or empty string that passes the weak validation (which only checks emptiness of some fields).

Fix: Use optional binding for the pin and show an invalid-PIN alert on failure; reject non-4-digit pins before networking.

Suggested test: Unit test with pinTextFeild.text = "12ab" and other fields filled: invoke didTapSignUp() and assert no crash and an "invalid pin" alert path (extract validation into a testable function).

Evidence:

````
                    let signUpResult = try await NetworkManager.shared.Signup(fullname: fullnameTextFeild.text!, email: emailTextFeild.text!, mobile: phoneTextFeild.text!, username: usernameTextFeild.text!, pin: Int(pinTextFeild.text!)!, passowrd: passwordTextFeild.text!)
````

## 3. [HIGH] Force unwrap of non-numeric PIN crashes sign-up

Location: `Expense Tracker/Controllers/Login SingUp/SingUpVC.swift:165` · Agents: quality

pinTextFeild has no numeric keyboard restriction (CustomTextFields init at line 36 sets no keyboardType), and its delegate allows up to 4 characters of any type (line 186). If the user types '12ab', Int(...) returns nil and the force unwrap crashes the app.

Fix: Use `guard let pin = Int(pinTextFeild.text ?? "") else { present validation error; return }` and set keyboardType = .numberPad on the PIN field.

Suggested test: UI test: enter letters in the PIN field and tap Sign up; app must show a validation alert instead of crashing.

Evidence:

````
                    let signUpResult = try await NetworkManager.shared.Signup(fullname: fullnameTextFeild.text!, email: emailTextFeild.text!, mobile: phoneTextFeild.text!, username: usernameTextFeild.text!, pin: Int(pinTextFeild.text!)!, passowrd: passwordTextFeild.text!)
````

## 4. [HIGH] 4-character limit applied to every signup field via shared UITextFieldDelegate

Location: `Expense Tracker/Controllers/Login SingUp/SingUpVC.swift:185` · Agents: tests

The delegate method caps ALL text fields in SingUpVC (full name, email, phone, username, password, confirm password) at 4 characters, making valid sign-up input impossible.

Fix: Apply the 4-char limit only to pinTextFeild (e.g., `if textField === pinTextFeild`).

Suggested test: Unit test: for each signup text field, simulate inserting a 10-character string via shouldChangeCharactersIn; assert it returns true for all fields except pinTextFeild (which returns false).

Evidence:

````
    func textField(_ textField: UITextField, shouldChangeCharactersIn range: NSRange, replacementString string: String) -> Bool {
        let maxLength = 4
````

## 5. [HIGH] Force unwrap crash on non-numeric amount in postTransaction

Location: `Expense Tracker/Controllers/Main/AddIncomeAndExpensesVC.swift:237` · Agents: tests

expensesAndIncomeTextField defaults to "$0" and uses a numberPad keyboard; the pre-seeded "$0" text or any non-numeric value causes Double(...)! to trap and crash the app before validation can reject it. Validation only checks emptiness, never numeric format.

Fix: Replace the force unwrap with optional binding (e.g., `guard let amount = Double(text)` else present an alert) and remove the "$0" seed text or strip "$` before conversion.

Suggested test: Unit test: create the view controller, set expensesAndIncomeTextField.text = "$0" and other fields non-empty, invoke postTransaction(), assert no fatal crash and that an alert is presented. Also test empty and "12.5a" inputs.

Evidence:

````
                    let result = try await NetworkManager.shared.makeTransaction(transectionTypeTextField.text!, titleTextField.text!, descriptionTextField.text!, Double(expensesAndIncomeTextField.text!)!)
````

## 6. [HIGH] Force-unwrapped Double conversion of '$0' default text crashes Save

Location: `Expense Tracker/Controllers/Main/AddIncomeAndExpensesVC.swift:237` · Agents: quality

expensesAndIncomeTextField starts with text "$0" (line 43) and only clears on begin editing. If the user fills other fields and taps Save without focusing the amount field, the Validate() check passes (text is non-empty) but Double("$0") is nil, crashing the app. Any non-numeric input also crashes.

Fix: Initialize the field with text "0" (no $ sign) or strip formatting before parsing: `guard let amount = expensesAndIncomeTextField.text.flatMap(Double.init)` else show a validation alert.

Suggested test: Unit test the parse path: Double("$0") is nil; UI test tapping Save without editing amount must show an alert, not crash.

Evidence:

````
                    let result = try await NetworkManager.shared.makeTransaction(transectionTypeTextField.text!, titleTextField.text!, descriptionTextField.text!, Double(expensesAndIncomeTextField.text!)!)
````

## 7. [HIGH] ProfileHeaderView.layoutSubviews re-loads nib and overwrites user's name with hardcoded value

Location: `Expense Tracker/Custom Views/UIView/ProfileHeaderView.swift:25` · Agents: quality

commonInit() is called from layoutSubviews, so every layout pass re-loads the nib via bundle.loadNibNamed and re-adds subviews (leak/perf issue), and it unconditionally sets user_fullName.text = "Abdorizak Abdalla Hassan" (line 60), overwriting the real name set by the convenience init at line 38. Users see the wrong name in the profile header after the first layout pass.

Fix: Move nib loading and constraint setup into a one-time setup called only from init; set user_fullName.text only in the convenience init, never in commonInit.

Suggested test: Instantiate ProfileHeaderView(user: "Alice", image: "x"), trigger layoutSubviews, and assert user_fullName.text == "Alice" and the nib was loaded once.

Evidence:

````
    override func layoutSubviews() {
        super.layoutSubviews()
        commonInit()
    }
````

## 8. [HIGH] Operator-precedence comma bug in sign-up all-empty check

Location: `Expense Tracker/Extentions/UIViewController+Ext.swift:73` · Agents: tests

The comma creates a tuple of the boolean expression and the confirmPass check; the if evaluates the first element, so confirmPass emptiness is ignored in the all-empty branch (covered incidentally by the later else-if, but the code is misleading and fragile).

Fix: Replace the comma with &&.

Suggested test: Compile-time/lint check; optionally unit test all fields empty returns .InValid("feilds cannot be Empty").

Evidence:

````
        if (fullname.text?.isEmpty)! && (email.text?.isEmpty)! && (mobile.text?.isEmpty)! && (username.text?.isEmpty)! && (pin.text?.isEmpty)! && (password.text?.isEmpty)!, (confirmPass.text?.isEmpty)! {
````

## 9. [HIGH] Password and credentials written to debug logs

Location: `Expense Tracker/Network Manager/AuthManager.swift:39` · Agents: security

The LoginBody struct contains the plaintext password and username/email. It is printed via print(), so plaintext credentials appear in Console/sysdiagnose logs on physical devices and in any attached debugger output. Logs can be collected by support tooling, synced off-device, or read by anything with access to the device console, exposing user passwords.

Fix: Remove all credential-logging statements (also the raw response prints in AuthManager and NetworkManager). If debug logging is needed, redact password/pin fields or gate logging behind a DEBUG-only custom formatter that masks secrets.

Suggested test: Run the login flow with a breakpoint-free release build on a device, capture Console output, and assert no request body containing the entered password or PIN appears in the log stream.

Evidence:

````
        print("DEBUG:\(body)")
````

## 10. [HIGH] userID captured once at singleton init, never updated after login

Location: `Expense Tracker/Network Manager/NetworkManager.swift:14` · Agents: quality

NetworkManager.shared is created when the app launches, before any login occurs, so userID is nil (or the previous session's value). After login, AuthManager.catchToken writes the new 'user_id' to UserDefaults, but this stored property is never refreshed. All dashboard/transaction requests then use the stale value or 'N/A' (line 27), and makeTransaction force-unwraps userID! (line 83) which crashes for a fresh login.

Fix: Make userID a computed property: `private var userID: String? { UserDefaults.standard.string(forKey: "user_id") }` so it is read at request time. Also replace `userID!` in makeTransaction with a guard that throws ExError.NotFound.

Suggested test: Launch app logged out, log in, then call getTransaction(); assert the request URL contains the new user id and makeTransaction does not crash.

Evidence:

````
    private let userID          = UserDefaults.standard.string(forKey: "user_id")
````

## 11. [MEDIUM] Early return in pinLogin leaves the loading overlay permanently displayed

Location: `Expense Tracker/Controllers/Login SingUp/LoginWithPinVC.swift:170` · Agents: quality

Actually showLoadingView() is called before the switch (line 172); if the concatenated text is non-numeric (paste of letters), guard returns without dismissLoadingView(), so the full-screen loading overlay blocks the UI indefinitely. (Note also the ordering: showLoadingView at 172 runs before validation branches.)

Fix: Validate/convert the PIN before calling showLoadingView(), and dismiss the loading view on every early-return path (use defer).

Suggested test: UI test: paste 'a' into a PIN field and tap Go; assert the loading view is removed and an error is shown within 1s.

Evidence:

````
        let pin = String(passInput1.text! + passInput2.text! + passInput3.text! + passInput4.text!)
        guard let pin = Int(pin) else { return }
        showLoadingView()
````

## 12. [MEDIUM] Duplicate constraint activation on every layout pass

Location: `Expense Tracker/Controllers/Main/HomeVC.swift:185` · Agents: quality

ConfigureHeaderElements() calls NSLayoutConstraint.activate with ~30 constraints and addSubViews each time. viewWillLayoutSubviews fires repeatedly (rotation, keyboard, alert presentation), creating thousands of duplicate conflicting constraints (AutoLayout warnings, degraded performance). Same anti-pattern in EditProfileVC (configImage in viewWillLayoutSubviews) and TransectionsVC (viewDidLayoutSubviews restarting chart animation).

Fix: Set up subviews and constraints once in viewDidLoad; in layout callbacks only adjust frame-dependent values (e.g. cornerRadius from bounds).

Suggested test: Trigger viewWillLayoutSubviews 5 times and assert NSLayoutConstraint.active count for the header is unchanged.

Evidence:

````
    override func viewWillLayoutSubviews() {
        super.viewWillLayoutSubviews()
        ConfigureHeaderElements()
    }
````

## 13. [MEDIUM] Face ID gate shows an alert on failure but does not lock the app

Location: `Expense Tracker/Custom Views/TabBar Controller/TabBarVC.swift:39` · Agents: security

When Face ID is enabled, TabBarVC's authenticateUser() prompts on viewDidAppear, but on failure it merely presents a dismissible alert; the authenticated TabBarVC and all its data remain fully visible and interactive. Anyone who fails or cancels biometrics (or uses a device where the prompt is dismissed) still has full access to the financial data, defeating the purpose of the biometric lock.

Fix: On authentication failure or cancel, dismiss the TabBarVC and return to the Login screen (or present a blocking overlay that cannot be dismissed without successful authentication). Consider re-prompting on foreground transitions as well.

Suggested test: UI test: with isFaceIDEnabled=true, launch to TabBarVC, cancel the biometric prompt, and assert the app transitions back to LoginVC (or a blocking view) and that transaction data is not reachable.

Evidence:

````
                        if !success {
                            // Handle authentication failure
                            let alert = UIAlertController(title: "Authentication Failed", message: "Please try again.", preferredStyle: .alert)
                            alert.addAction(UIAlertAction(title: "OK", style: .default, handler: nil))
                            self?.present(alert, animated: true, completion: nil)
                        }
````

## 14. [MEDIUM] Broken boolean expression in sign-up validation (comma operator)

Location: `Expense Tracker/Extentions/UIViewController+Ext.swift:73` · Agents: security

The trailing `!, (confirmPass.text?.isEmpty)!` is a comma expression, not a logical AND, so the 'all fields empty' check ignores confirmPass and only evaluates the last expression for the branch condition. This is a correctness defect in input validation for account creation, and the broader signup flow relies only on emptiness checks — the Validation class (email/phone/password strength regexes in ValidationTextField.swift) is never invoked, so weak passwords and malformed emails/phones are accepted client-side.

Fix: Fix the condition to use && throughout, and call Validation.validateEmailId/validaPhoneNumber/validatePassword before sending the signup request.

Suggested test: Unit test: set all fields empty except confirmPass; current code falls through individual checks. Also submit a signup with password 'a' and email 'not-an-email'; assert the client rejects with InValid rather than calling the network.

Evidence:

````
        if (fullname.text?.isEmpty)! && (email.text?.isEmpty)! && (mobile.text?.isEmpty)! && (username.text?.isEmpty)! && (pin.text?.isEmpty)! && (password.text?.isEmpty)!, (confirmPass.text?.isEmpty)! {
````

## 15. [MEDIUM] Comma operator makes confirm-password emptiness check ineffective

Location: `Expense Tracker/Extentions/UIViewController+Ext.swift:73` · Agents: quality

The comma before (confirmPass.text?.isEmpty)! is the comma operator/expression separator, not a logical AND. The confirmPass term is not part of the if condition; it is merely evaluated for side effects. The combined 'all empty' branch is therefore tested without confirmPass, producing inconsistent error messages (it can report 'fields cannot be Empty' when confirmPass is filled, or fall through the else-chain incorrectly).

Fix: Replace the comma with && so all seven fields are tested together.

Suggested test: Unit test: fill all fields except confirmPass and one other; assert the returned message matches the expected per-field branch.

Evidence:

````
        if (fullname.text?.isEmpty)! && (email.text?.isEmpty)! && (mobile.text?.isEmpty)! && (username.text?.isEmpty)! && (pin.text?.isEmpty)! && (password.text?.isEmpty)!, (confirmPass.text?.isEmpty)! {
````

## 16. [MEDIUM] try? on httpBody silently drops encode errors, sending empty request bodies

Location: `Expense Tracker/Network Manager/AuthManager.swift:43` · Agents: quality

Anti-pattern: swallowed exception. If JSONEncoder fails (or a future field becomes non-encodable), httpBody is nil and the server receives a bodyless POST, returning a confusing 400/invalidResponse error with no local diagnostic. Same pattern at line 69 and NetworkManager.swift line 138.

Fix: Use `request.httpBody = try JSONEncoder().encode(body)` so failures propagate as thrown errors, and add encoding-specific error logging.

Suggested test: Inject a body that fails to encode (e.g. invalid Date) and assert login() throws a descriptive error rather than a server 'invalidResponse'.

Evidence:

````
        request.httpBody = try? JSONEncoder().encode(body)
````

## 17. [MEDIUM] Access token stored in UserDefaults instead of Keychain

Location: `Expense Tracker/Network Manager/AuthManager.swift:85` · Agents: security

The bearer access token and user identifier are persisted in UserDefaults, which is an unencrypted plist in the app container. On a jailbroken device, via an unencrypted iTunes-style backup, or on a shared/compromised device, the token can be extracted and used directly against the API (NetworkManager sends it as `Bearer \(token)`) to fully impersonate the user.

Fix: Store the access token (and refresh material) in the iOS Keychain with `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly`. Keep only non-sensitive flags (e.g., hasOnboarded, isFaceIDEnabled) in UserDefaults.

Suggested test: Inspect the app's Library/Preferences plist on a test device after login; assert the access_token key is absent and a Keychain item exists with device-only accessibility.

Evidence:

````
        UserDefaults.standard.setValue(result.accessToken, forKey: "access_token")
        UserDefaults.standard.setValue(result.userInfo, forKey: "user_id")
````

## 18. [MEDIUM] Logout does not clear user_id; NetworkManager caches it at init causing stale identity

Location: `Expense Tracker/Network Manager/NetworkManager.swift:14` · Agents: security

NetworkManager is a singleton whose `userID` is captured once when the singleton is first created. After logout, AuthManager.SingOut() (AuthManager.swift:90) only clears "access_token", not "user_id", and because the singleton persists, the old user's ID remains cached even after a new user logs in. All subsequent dashboard/transaction calls then request data for the previous user (URLs embed userID, e.g. `transactions/\(userID ?? "N/A")`), leaking one user's financial data into another user's session if the app process is reused.

Fix: Read user_id dynamically from UserDefaults (or hold it in a session object reset on login/logout), and clear both access_token and user_id in SingOut().

Suggested test: Unit test: log in as user A, log out, log in as user B in the same process; assert getTransaction()/getDashboardData() build request URLs containing B's user id, and assert UserDefaults has no stale user_id after logout.

Evidence:

````
    private let userID          = UserDefaults.standard.string(forKey: "user_id")
````

## 19. [MEDIUM] Decode errors are masked as generic inValidData, discarding diagnostics

Location: `Expense Tracker/Network Manager/NetworkManager.swift:33` · Agents: quality

Overly broad exception handling: the underlying DecodingError (which key failed, debug description) is swallowed. This makes backend schema drift impossible to diagnose and produces a misleading user message ('data received was Invalid'). Pattern repeated in every method of both NetworkManager and AuthManager.

Fix: Log the caught error before rethrowing (e.g. `print("Decode error: \(error)")`), or wrap it: `throw ExError.decodingError` while attaching the underlying error via a localized description.

Suggested test: Feed malformed JSON to getDashboardData(); assert the thrown error carries the original DecodingError context in logs/description.

Evidence:

````
        do {
            return try decoder.decode(UserBalanceIncomeExpense.self, from: data)
        } catch {
            throw ExError.inValidData
        }
````

## 20. [MEDIUM] No tests exist anywhere in the snapshot

Location: `Expense Tracker/Utilits/ValidationTextField.swift:13` · Agents: tests

The repository snapshot contains no test target or test files. Pure logic such as Validation, Double.formatNumber, UIColor(hex:), and UIViewController.Validate overloads are unit-testable but untested; these are exactly where the defects above (PIN/amount parsing, validation gaps) would have been caught.

Fix: Add an XCTest target with unit tests for Validation regexes (valid/invalid name, phone, email, password, username), Double.formatNumber boundaries (999, 1000, 1_000_000, negatives), and hex color parsing (6/8-length strings).

Suggested test: XCTest: `XCTAssertTrue(Validation.validate.validateEmailId("a@b.co"))`, `XCTAssertFalse(...("bad"))`; formatNumber: 999 -> "999.0", 1500 -> "1.5K", -2000000 -> "-2.0M".

Evidence:

````
    func validateName(name: String) ->Bool {
````

## 21. [LOW] Duplicated login success/error handling logic across LoginVC and LoginWithPinVC

Location: `Expense Tracker/Controllers/Login SingUp/LoginWithPinVC.swift:177` · Agents: quality

Duplicated business logic: the full 'call auth, check status, present TabBarVC full-screen, dismiss loading, map ExError vs other errors' flow is copy-pasted in LoginVC.loginBtnClicked (lines 67-91), LoginWithPinVC.pinLogin, and SingUpVC.didTapSignUp. A fix to one path (e.g. the loading-view dismissal bug) will not reach the others, and the copies have already diverged (the 😁 suffix, error.rawValue vs plain interpolation).

Fix: Extract a shared helper (e.g. on DataLoadingVC) such as `func handleAuthResult(_ result: LoginResponse)` and `func handleAuthError(_ error: Error)` used by all three call sites.

Suggested test: Refactor test: simulate a non-200 login response for both password and PIN flows and assert identical alert presentation and loading dismissal.

Evidence:

````
                        let result = try await AuthManager.shared.login(with: pin)
                        if result.status != 200 {
                            presentAlertOnMainThread(title: "Opps!", message: "\(result.message ?? "N/A") 😁", btnTitle: "ok")
````

## 22. [LOW] Change Password 'Save' action is unimplemented

Location: `Expense Tracker/Controllers/ProfileViews/ChangePasswordVC.swift:115` · Agents: security

The Save bar button does nothing; users cannot change their password, and there is no client-side check of new/confirm password match here (unlike signup). Not a vulnerability by itself, but a security feature that is advertised in the UI and silently absent.

Fix: Implement the handler: validate current/new/confirm fields, verify new password strength with Validation.validatePassword, and call a password-change endpoint that requires the current password.

Suggested test: UI test: fill all three fields with non-matching new/confirm passwords, tap Save, and assert a validation alert is shown and no network call is made.

Evidence:

````
    @objc func didTapSave() {
        // this will check first current password the will change password by checking password
        
    }
````

## 23. [LOW] Edit Profile save button has no action and selected image is never uploaded

Location: `Expense Tracker/Controllers/ProfileViews/EditProfileVC.swift:302` · Agents: security

configSavebtn() sets constraints but never adds a target/action, so edits (name, email, phone, avatar image) are silently discarded when the user taps Save. The avatar image set via the pickers (lines 322/336) is only displayed locally.

Fix: Wire the Save button to validation plus an authenticated profile-update API call, including image upload.

Suggested test: UI test: modify the fullname field, tap Save, and assert a network request is initiated (or a validation error is surfaced) rather than nothing happening.

Evidence:

````
    func configSavebtn() {
        saveBtn.setTitle("Save", for: .normal)
        contentView.addSubview(saveBtn)
````

## 24. [LOW] Profile header hardcodes developer's name, overriding real user data

Location: `Expense Tracker/Custom Views/UIView/ProfileHeaderView.swift:60` · Agents: security

commonInit() is also re-invoked from layoutSubviews(), overwriting the actual user's full name (set via the convenience init at line 38) with a hardcoded developer name on every layout pass. This is a correctness/quality defect in displaying user data.

Fix: Remove the hardcoded assignment and don't call commonInit() from layoutSubviews(); perform nib loading/subview setup once in init.

Suggested test: Instantiate ProfileHeaderView(user: "Test User", ...) in a unit test, trigger layoutSubviews(), and assert user_fullName.text remains "Test User".

Evidence:

````
        user_fullName.text = "Abdorizak Abdalla Hassan"
````

## 25. [LOW] NetworkManager userID captured once at singleton init

Location: `Expense Tracker/Network Manager/NetworkManager.swift:14` · Agents: tests

userID is read when the singleton is created (first access, possibly before login writes "user_id"), so subsequent authenticated requests can use a stale/nil userID ("N/A") for the lifetime of the process. Logout followed by a different login in the same session would keep the old user id.

Fix: Make userID a computed property reading UserDefaults at call time.

Suggested test: Unit test: set UserDefaults "user_id" = nil, touch NetworkManager.shared (force init), then set "user_id" = "user1"; assert the request URL for getTransaction contains "user1" (requires computed property; currently would contain "N/A").

Evidence:

````
    private let userID          = UserDefaults.standard.string(forKey: "user_id")
````

## 26. [INFO] Server-supplied avatar path concatenated into URL without validation

Location: `Expense Tracker/Controllers/Main/HomeVC.swift:216` · Agents: security

The avatar value from the API is string-concatenated into an image URL. A compromised or malicious backend (or a MITM if TLS were ever downgraded) could supply values such as `@evil.com/x` or path fragments causing URLSession to follow an attacker-chosen host, exfiltrating the bearer-token-adjacent session context or loading arbitrary content. Impact is limited because it only downloads an image, but URL construction is unvalidated.

Fix: Parse the avatar value with URL(string:relativeTo:) or URLComponents against a fixed base URL, and reject values that resolve to a different host or contain suspicious characters.

Suggested test: Unit test downloadImage URL construction with avatar values like `@evil.com/a.png`, `//evil.com/a.png`, and `../etc`; assert each is rejected and only same-host paths are fetched.

Evidence:

````
        userImage.downloadImage(fromURL: "https://expensetracker.abdorizak.dev/" + data.user.avatar)
````

## Review limitations

- quality: ok
  - AuthManager.SingOut only clears 'access_token', not 'user_id' or 'isFaceIDEnabled'; combined with the stale userID finding this leaves orphaned state, but user-visible impact of user_id specifically is covered by finding 1.
  - LoginWithPinVC presents the PIN screen with modalPresentationStyle = .popover (LoginVC line 101), which renders oddly on iPhone, but this is a style/layout issue rather than a correctness defect.
  - Constants.swift device checks conflate several devices (e.g. isiPhoneX == isiPhonePro == isiPhoneMini all test maxLength 812.0), so device-specific constraint branches may not match the intended device; UI impact not verified.
  - NetworkManager decoder uses .convertFromSnakeCase while Transaction declares CodingKeys explicitly; this combination appears consistent for the shown fields, but custom snake_case keys like "userincome" could behave unexpectedly if the server changes casing — not verifiable without the API.
  - Corrected 1 source citation(s) using unambiguous matches in the cited file; exact source excerpts retained.
- security: ok
  - Only the client-side Swift snapshot was reviewed; the backend API (rate limiting, PIN lockout, token TTL, password hashing) cannot be verified from this data, so PIN and token findings are inferred from client behavior.
  - No Info.plist, ATS configuration, or dependency manifests (Package.resolved / Podfile.lock) were included, so insecure-dependency and TLS-configuration review was not possible.
  - UserDefaults on a non-jailbroken, iOS 13+ device with a passcode is encrypted at rest; the token-exposure risk primarily applies to jailbroken devices, unencrypted backups, or forensic access.
- tests: ok
  - No test target or existing tests were included in the snapshot, so coverage of production behavior could not be evaluated against actual test code; findings are from static inspection only.
  - Supporting files referenced but not supplied (e.g., API server behavior, Images assets, ProfileHeaderView XIB, MockData images) could not be verified.
  - Runtime UI behavior (Auto Layout constraint conflicts, popover presentation on iPhone) cannot be confirmed statically.
  - Discarded unverified finding: Transaction validation never checks the title field
  - Discarded unverified finding: Missing empty-state/error-path tests for HomeVC data loading
  - Discarded unverified finding: TransectionsVC empty-state branches unreachable for expense-only users
  - Discarded unverified finding: PIN login silently returns leaving stale loading state risk and no partial-pin alert
  - Corrected 4 source citation(s) using unambiguous matches in the cited file; exact source excerpts retained.
