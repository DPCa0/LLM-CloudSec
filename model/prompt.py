import json

judgement_prompt ='''
You are a professional vulnerability analyzer. I will give you a piece of C/C++ code and you have to determine if there are flaws in the code I provide. Only the security of this code itself is considered, and the security of other functions called and vulnerabilities that may result from operations are not considered.
The criterion is whether it can be used maliciously. Please only consider the security of the code itself and determine as a whole if there are flaws in the code.

Response Format:
Ture: If there is a flaw in the code.
False: If there is no flaw in the code.
'''

classify_prompt = '''
You are a professional vulnerability analyzer. I will give you a piece of C/C++ code with flaws.
For each flaw, you have to determine the category of the flaw based on the code I provide.
The list is provided below.
Out-of-bounds Write: The product writes data past the end, or before the beginning, of the intended buffer.
Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting'): The product does not neutralize or incorrectly neutralizes user-controllable input before it is placed in output that is used as a web page that is served to other users.
Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection'): The product constructs all or part of an SQL command using externally-influenced input from an upstream component, but it does not neutralize or incorrectly neutralizes special elements that could modify the intended SQL command when it is sent to a downstream component.
Use After Free: Referencing memory after it has been freed can cause a program to crash, use unexpected values, or execute code.
Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection'): The product constructs all or part of an OS command using externally-influenced input from an upstream component, but it does not neutralize or incorrectly neutralizes special elements that could modify the intended OS command when it is sent to a downstream component.
Improper Input Validation: The product receives input or data, but it does not validate or incorrectly validates that the input has the properties that are required to process the data safely and correctly.
Out-of-bounds Read: The product reads data past the end, or before the beginning, of the intended buffer.
Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal'): The product uses external input to construct a pathname that is intended to identify a file or directory that is located underneath a restricted parent directory, but the product does not properly neutralize special elements within the pathname that can cause the pathname to resolve to a location that is outside of the restricted directory.
Cross-Site Request Forgery (CSRF): The web application does not, or can not, sufficiently verify whether a well-formed, valid, consistent request was intentionally provided by the user who submitted the request.
Unrestricted Upload of File with Dangerous Type: The product allows the attacker to upload or transfer files of dangerous types that can be automatically processed within the product's environment.
Missing Authorization: The product does not perform an authorization check when an actor attempts to access a resource or perform an action.
NULL Pointer Dereference: A NULL pointer dereference occurs when the application dereferences a pointer that it expects to be valid, but is NULL, typically causing a crash or exit.
Improper Authentication: When an actor claims to have a given identity, the product does not prove or insufficiently proves that the claim is correct.
Integer Overflow or Wraparound: The product performs a calculation that can produce an integer overflow or wraparound, when the logic assumes that the resulting value will always be larger than the original value. This can introduce other weaknesses when the calculation is used for resource management or execution control.
Deserialization of Untrusted Data: The product deserializes untrusted data without sufficiently verifying that the resulting data will be valid.
Improper Neutralization of Special Elements used in a Command ('Command Injection'): The product constructs all or part of a command using externally-influenced input from an upstream component, but it does not neutralize or incorrectly neutralizes special elements that could modify the intended command when it is sent to a downstream component.
Improper Restriction of Operations within the Bounds of a Memory Buffer: The product performs operations on a memory buffer, but it can read from or write to a memory location that is outside of the intended boundary of the buffer.
Use of Hard-coded Credentials: The product contains hard-coded credentials, such as a password or cryptographic key, which it uses for its own inbound authentication, outbound communication to external components, or encryption of internal data.
Server-Side Request Forgery (SSRF): The web server receives a URL or similar request from an upstream component and retrieves the contents of this URL, but it does not sufficiently ensure that the request is being sent to the expected destination.
Missing Authentication for Critical Function: The product does not perform any authentication for functionality that requires a provable user identity or consumes a significant amount of resources.
Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition'): The product contains a code sequence that can run concurrently with other code, and the code sequence requires temporary, exclusive access to a shared resource, but a timing window exists in which the shared resource can be modified by another code sequence that is operating concurrently.
Improper Privilege Management: The product does not properly assign, modify, track, or check privileges for an actor, creating an unintended sphere of control for that actor.
Improper Control of Generation of Code ('Code Injection'): The product constructs all or part of a code segment using externally-influenced input from an upstream component, but it does not neutralize or incorrectly neutralizes special elements that could modify the syntax or behavior of the intended code segment.
Incorrect Authorization: The product performs an authorization check when an actor attempts to access a resource or perform an action, but it does not correctly perform the check. This allows attackers to bypass intended access restrictions.
Incorrect Default Permissions: During installation, installed file permissions are set to allow anyone to modify those files.

Response Format:
flaw category: The category of the flaw.
flaw code: The code of the flaw.
'''


# with open('../scripts/cwe_data.json', 'r') as f:
#     cwe_list = json.load(f)
#
# for cwe in cwe_list:
#     print(f"{cwe['name']}: {cwe['description']}")
