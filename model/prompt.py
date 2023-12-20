import json


classify1_prompt = '''
You are a professional vulnerability analyzer. I will give you a piece of C/C++ code with flaws.
You have to judge the category of the flaw based on the code I provide.
The category list is:
15,External Control of System or Configuration Setting
23,Relative Path Traversal
36,Absolute Path Traversal
78,Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')
90,Improper Neutralization of Special Elements used in an LDAP Query ('LDAP Injection')
121,Stack-based Buffer Overflow
122,Heap-based Buffer Overflow
123,Write-what-where Condition
124,Buffer Underwrite ('Buffer Underflow')
126,Buffer Over-read
127,Buffer Under-read
134,Use of Externally-Controlled Format String
176,Improper Handling of Unicode Encoding
190,Integer Overflow or Wraparound
191,Integer Underflow (Wrap or Wraparound)
194,Unexpected Sign Extension
195,Signed to Unsigned Conversion Error
197,Numeric Truncation Error
252,Unchecked Return Value
253,Incorrect Check of Function Return Value
256,Plaintext Storage of a Password
259,Use of Hard-coded Password
272,Least Privilege Violation
273,Improper Check for Dropped Privileges
321,Use of Hard-coded Cryptographic Key
338,Use of Cryptographically Weak Pseudo-Random Number Generator (PRNG)
364,Signal Handler Race Condition
366,Race Condition within a Thread
369,Divide By Zero
377,Insecure Temporary File
390,Detection of Error Condition Without Action
391,Unchecked Error Condition
397,Declaration of Throws for Generic Exception
400,Uncontrolled Resource Consumption
401,Missing Release of Memory after Effective Lifetime
404,Improper Resource Shutdown or Release
415,Double Free
416,Use After Free
427,Uncontrolled Search Path Element
457,Use of Uninitialized Variable
459,Incomplete Cleanup
464,Addition of Data Structure Sentinel
467,Use of sizeof() on a Pointer Type
476,NULL Pointer Dereference
479,Signal Handler Use of a Non-reentrant Function
480,Use of Incorrect Operator
511,Logic/Time Bomb
526,Cleartext Storage of Sensitive Information in an Environment Variable
546,Suspicious Comment
563,Assignment to Variable without Use
587,Assignment of a Fixed Address to a Pointer
588,Attempt to Access Child of a Non-structure Pointer
590,Free of Memory not on the Heap
591,Sensitive Data Storage in Improperly Locked Memory
606,Unchecked Input for Loop Condition
617,Reachable Assertion
665,Improper Initialization
672,Operation on a Resource after Expiration or Release
675,Multiple Operations on Resource in Single-Operation Context
758,Reliance on Undefined
761,Free of Pointer not at Start of Buffer
762,Mismatched Memory Management Routines
773,Missing Reference to Active File Descriptor or Handle
775,Missing Release of File Descriptor or Handle after Effective Lifetime
680,Integer Overflow to Buffer Overflow
789,Memory Allocation with Excessive Size Value
690,Unchecked Return Value to NULL Pointer Dereference

For the vulnerability that exists in this code, you need to decide on one or more categories that fit the category of the vulnerability in the code.
Response format is the same as the list above, if there is no flaw in the code, response null:
category number, flaw category
'''

classify_empty_prompt = '''
You are a professional vulnerability analyzer. I will give you a piece of C/C++ code with flaws.
You have to judge the category of the flaw based on the code I provide.
The category list is Common Weakness Enumeration (CWE) list, which is a list of software weaknesses.
For the vulnerability that exists in this code, you need to decide on one or more categories that fit the category of the vulnerability in the code.
If there is no flaw in the code, response null.
Response format:
category number, flaw category
'''


insert_prompt = '''You are a professional vulnerability analyzer. I will give you a piece of C/C++ code with flaws.
I will give you one or some categories of the flaw in the code, and you have to determine the which part of code that may cause the flaws. 
The potential flaw type and description are:

response format:
flaw category, corresponding code that may cause the flaw'''






judgement_prompt ='''
You are a professional vulnerability analyzer. I will give you a piece of C/C++ code and you have to determine if there are flaws in the code I provide. Only the security of this code itself is considered, and the security of other functions called and vulnerabilities that may result from operations are not considered.
The criterion is whether it can be used maliciously. Please only consider the security of the code itself and determine as a whole if there are flaws in the code.

Response Format:
Ture: If there is a flaw in the code.
False: If there is no flaw in the code.
'''

