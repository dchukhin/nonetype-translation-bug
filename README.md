To reproduce the bug:

1. run `bash setup.sh`
2. run `python manage.py runserver`
3. open http://localhost:8000/admin/
4. log in as admin / admin
5. go to Pages → Demo Bug Page, and select Translate in the page menu
6. select French and click Submit
7. observe the TypeError in the server console
