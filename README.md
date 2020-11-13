Screen shots for the wep app :
https://drive.google.com/drive/folders/11f4VGTEAGC3FXqWq6mUW96lMIqeXReF7


Steps to run web app on local machine :

1)  download python 3 from  https://www.python.org/downloads/
2)  install django using pip install Django== 2.2.7
3)  download git repository using url  https://github.com/MahendraKotapati/TopRepos.git
4)  extract files 
    and go to TopRepos-master--->TopRepos-master->TopRepos->views.py 

5) in views.py at top assign  token = ' your github token '
    token is taken from your github account 

    generating github token :
      i)go to (in github account) settings ->developer settings-->personal access tokens -->generate new token
        makesure to check the check box repo
        generate token
 6) assign your github token in value in views.py 
      token = ' xxxxxxxxxxxx '
7)  go to TopRepos-master--->TopRepos-master in command line 
     run command  py manage.py runserver
8) then access web app using  http://127.0.0.1:8000/

 				

