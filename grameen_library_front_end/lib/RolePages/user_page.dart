import 'package:flutter/material.dart';
import 'package:grameen_library_front_end/parts.dart';
import 'package:shared_preferences/shared_preferences.dart';

class UserPage extends StatefulWidget {
  @override
  _UserPageState createState() => _UserPageState();
}

class _UserPageState extends State<UserPage> {
  String username;
  String id;
  SharedPreferences sharedPreferences;
  @override
  void initState(){
    setData();
  }

  void setData() async{
    sharedPreferences = await SharedPreferences.getInstance();
    setState(() {
      username = sharedPreferences.getString("username") ?? "Error";
      id=sharedPreferences.getString("userid") ?? "Error";
      print(username);
    });
  }
  List<Widget> _getBooks() {
    //TODO get the books the user has borrowed from the database and return them as a table widget
    return <Widget>[
      Container(height: 200.0),
      Text('Return books on time',
          style: TextStyle(
            color: Colors.black,
            fontSize: 24.0,
          ))
    ];
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            LeftSide(),
            Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Container(
                  alignment: Alignment.topLeft,
                  child: Text(
                    'List of Books Borrowed',
                    style: TextStyle(
                      fontSize: 24.0,
                      color: Colors.black,
                    ),
                  ),
                ),
                SizedBox(height: MediaQuery.of(context).size.height * 0.03),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: _getBooks(),
                ),
              ],
            ),
            RightSide(
              username: username,
            ),
          ],
        ),
      ),
    );
  }
}

class RightSide extends StatelessWidget {
  String username;

  RightSide({Key key, this.username}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Flexible(
      child :Container(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Logged in as\n$username',
              style: TextStyle(
                color: Colors.black,
                fontSize: 24.0,
              ),
            ),
            SizedBox(height: MediaQuery.of(context).size.height * 0.05),
            Container(
              margin: EdgeInsets.symmetric(
                  horizontal: MediaQuery.of(context).size.width * 0.05),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.start,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  InkWell(
                    onTap: () {
                      Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (context) => BookList(books: []),
                        ),
                      );
                    },
                    child: Container(
                      child: Text(
                        'Borrowed Books List',
                        style: TextStyle(
                          color: Colors.black,
                          fontSize: 20.0,
                        ),
                      ),
                    ),
                  ),
                  SizedBox(height: MediaQuery.of(context).size.height * 0.03 ),
                  InkWell(
                    onTap: () {
                      Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (context) => ContactDetails(),
                        ),
                      );
                    },
                    child: Container(
                      child: Text(
                        'User Contact Details',
                        style: TextStyle(
                          color: Colors.black,
                          fontSize: 20.0,
                        ),
                      ),
                    ),
                  ),
                  SizedBox(height: MediaQuery.of(context).size.height * 0.03 ),
                  InkWell(
                    onTap: () {
                      Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (context) => ChangeUserDetails(),
                        ),
                      );
                    },
                    child: Container(
                      child: Text(
                        'Change User Details',
                        style: TextStyle(
                          color: Colors.black,
                          fontSize: 20.0,
                        ),
                      ),
                    ),
                  ),
                  SizedBox(height: MediaQuery.of(context).size.height * 0.03 ),
                  InkWell(
                    onTap: () {
                      Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (context) => DosAndDonts(),
                        ),
                      );
                    },
                    child: Container(
                      child: Text(
                        'Do\'s and Dont\'s',
                        style: TextStyle(
                          color: Colors.black,
                          fontSize: 20.0,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            )
          ],
        ),
    )
    );
  }
}

class BookList extends StatelessWidget {
  List<String> books;

  BookList({this.books});

  @override
  Widget build(BuildContext context) {
    //TODO return the list of books in a suitable format in this page(preferable to use list view)
    return Scaffold(
      body: Flexible(
        child : Container(
        child: Center(
          child: Text('Books List Page'),
        )
      ),
    )
    );
  }
}

class ContactDetails extends StatelessWidget {
  Map user_details;

  ContactDetails({this.user_details});

  @override
  Widget build(BuildContext context) {
    //TODO get the user details from the login page give them as an input to this widget
    //TODO display the user details in a neat and minimalistic fashion
    return Scaffold(
      body: Flexible(
        child: Container(
        child: Center(
          child: Text('Contact Details Page'),
        )
      ),
    )
    );
  }
}

class ChangeUserDetails extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    //TODO come up with a way to let the user change his details/credentials
    return Scaffold(
      body: Flexible(
        child:Container(
        child: Center(
          child: Text('Change User Details Page')
        )
      )
    )
    );
  }
}

class DosAndDonts extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    //TODO fill in the static details for this page
    return Scaffold(
        body: Flexible(
          child: Container(
            child: Center(
                child: Text('Do\'s and Dont\'s static page'),
            ),
        ),
    )
    );
  }
}


