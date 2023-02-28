prefix: /auth/

login: /login <POST Method>
parameters:
*username:String -> Default value = None || Optional || min_length=3, max_length=32
*password:String -> min_length=3, max_length=32
\*email:String -> Default value = None || Optional || min_length=3, max_length=32

verify: /verify <POST Method>
headers:
Authorization: bearer token
