# secureCloud-viewer
Web application that decrypts content stored on (potentially any) cloud, and presents it to user.

## Configure Run and Debug from PyCharm
1 In "PyCharm Professional" open "File"->"Settings"
2 "Languages & Frameworks"->"Python Template Languages"
3 From "Template language" drop-down choose "Django"
4 In "Template language"->"Django" check "Enable Django Support"
5 Set "Django project root" to project root
6 Set "Settings" to "(project_name)\settings.py"
7 Set "Manage scripts" to "manage.py"
8 In "PyCharm Professional" open "Run"->"Edit Configurations..."
9 Add new "Django server"
10 Type "Host": 127.0.0.1 and "Port": arbitrary value (recommended: 8000)
<br/><br/>
Now you can Run and Debug server from PyCharm

## Software requirements
- PyCharm Professional 2016.1 (https://www.jetbrains.com/pycharm/download/#section=windows)
- Django 1.9 (in cmd run as administrator: "pip install django=1.9")
