import 'dart:html';

import 'package:flutter/material.dart';

import 'package:grameen_library_front_end/parts.dart';

class PanchayatPage extends StatelessWidget {
  String username;

  PanchayatPage({this.username = 'DefaultPanchayat'});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        child: Row(
          children: [
            LeftSide(),
            SizedBox(width: MediaQuery.of(context).size.width * 0.1),
            Content(),
            RightSide(username: this.username),
          ],
        ),
      ),
    );
  }
}

class Content extends StatefulWidget {
  @override
  _ContentState createState() => _ContentState();
}

class _ContentState extends State<Content> {
  @override
  Widget build(BuildContext context) {
    BoxDecoration _decoration =
        DecorateField().decoration3(MediaQuery.of(context).size);
    return Container(
      width: MediaQuery.of(context).size.width * 0.5,
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Panchayat Dashboard',
                  style: TextStyle(
                    color: Colors.black,
                    fontSize: 30.0,
                    fontWeight: FontWeight.bold,
                    fontStyle: FontStyle.italic,
                  ),
                ),
                SizedBox(height: MediaQuery.of(context).size.height * 0.05),
                Row(
                  children: [
                    Container(
                      width: MediaQuery.of(context).size.width * 0.12,
                      child: Text(
                        'Search User',
                        style: TextStyle(
                          color: Colors.black,
                          fontSize: 24.0,
                        ),
                      ),
                    ),
                    SizedBox(
                      width: MediaQuery.of(context).size.width * 0.1,
                    ),
                    Container(
                      constraints: BoxConstraints(
                        minHeight: MediaQuery.of(context).size.height * 0.05,
                        minWidth: MediaQuery.of(context).size.width * 0.2,
                      ),
                      decoration: _decoration,
                    ),
                  ],
                ),
                SizedBox(height: MediaQuery.of(context).size.height * 0.03),
                Row(
                  children: [
                    Container(
                      width: MediaQuery.of(context).size.width * 0.12,
                      child: Text(
                        'Issue/Return/Renew',
                        style: TextStyle(
                          color: Colors.black,
                          fontSize: 24.0,
                        ),
                      ),
                    ),
                    SizedBox(
                      width: MediaQuery.of(context).size.width * 0.1,
                    ),
                    Container(
                      constraints: BoxConstraints(
                        minHeight: MediaQuery.of(context).size.height * 0.05,
                        minWidth: MediaQuery.of(context).size.width * 0.2,
                      ),
                      decoration: _decoration,
                    ),
                  ],
                ),
                SizedBox(height: MediaQuery.of(context).size.height * 0.03),
                Row(
                  children: [
                    Container(
                      width: MediaQuery.of(context).size.width * 0.12,
                      child: Text(
                        'Book ID',
                        style: TextStyle(
                          color: Colors.black,
                          fontSize: 24.0,
                        ),
                      ),
                    ),
                    SizedBox(
                      width: MediaQuery.of(context).size.width * 0.1,
                    ),
                    Container(
                      constraints: BoxConstraints(
                        minHeight: MediaQuery.of(context).size.height * 0.05,
                        minWidth: MediaQuery.of(context).size.width * 0.2,
                      ),
                      decoration: _decoration,
                    ),
                  ],
                ),
                SizedBox(height: MediaQuery.of(context).size.height * 0.03),
                Row(
                  children: [
                    Container(
                      width: MediaQuery.of(context).size.width * 0.12,
                      child: Text(
                        'Issue Date',
                        style: TextStyle(
                          color: Colors.black,
                          fontSize: 24.0,
                        ),
                      ),
                    ),
                    SizedBox(
                      width: MediaQuery.of(context).size.width * 0.1,
                    ),
                    Container(
                      constraints: BoxConstraints(
                        minHeight: MediaQuery.of(context).size.height * 0.05,
                        minWidth: MediaQuery.of(context).size.width * 0.2,
                      ),
                      decoration: _decoration,
                    ),
                  ],
                ),
                SizedBox(height: MediaQuery.of(context).size.height * 0.03),
                Row(
                  children: [
                    Container(
                      width: MediaQuery.of(context).size.width * 0.12,
                      child: Text(
                        'Return Date',
                        style: TextStyle(
                          color: Colors.black,
                          fontSize: 24.0,
                        ),
                      ),
                    ),
                    SizedBox(
                      width: MediaQuery.of(context).size.width * 0.1,
                    ),
                    Container(
                      constraints: BoxConstraints(
                        minHeight: MediaQuery.of(context).size.height * 0.05,
                        minWidth: MediaQuery.of(context).size.width * 0.2,
                      ),
                      decoration: _decoration,
                    ),
                  ],
                ),
                SizedBox(height: MediaQuery.of(context).size.height * 0.07),
              ],
            ),
          ),
          Row(
            children: [
              SizedBox(
                width: MediaQuery.of(context).size.width * 0.1,
              ),
              Container(
                width: MediaQuery.of(context).size.width * 0.1,
                height: MediaQuery.of(context).size.height * 0.04,
                child: RaisedButton(
                  child: Text('Submit'),
                  onPressed: () {
                    print('submitted');
                  },
                ),
              ),
            ],
          )
        ],
      ),
    );
  }
}

class RightSide extends StatelessWidget {
  String username;

  RightSide({this.username});

  @override
  Widget build(BuildContext context) {
    Size sz = MediaQuery.of(context).size;

    return Container(
      padding: EdgeInsets.symmetric(horizontal: sz.width * 0.04),
      alignment: Alignment.center,
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            child: Text(
              'Logged in as\n$username',
              style: TextStyle(
                color: Colors.black,
                fontSize: 24.0,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
          SizedBox(height: sz.height * 0.1),
          Column(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              InkWell(
                onTap: () {
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => BooksList(),
                    ),
                  );
                },
                child: Container(
                  child: Text(
                    'Books List',
                    style: TextStyle(
                      color: Colors.black,
                      fontSize: 24.0,
                    ),
                  ),
                ),
              ),
              SizedBox(height: sz.height * 0.03),
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
                    'User Details',
                    style: TextStyle(
                      color: Colors.black,
                      fontSize: 24.0,
                    ),
                  ),
                ),
              ),
              SizedBox(height: sz.height * 0.03),
              InkWell(
                onTap: () {
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => PanchayatDetails(),
                    ),
                  );
                },
                child: Container(
                  child: Text(
                    'Panchayat Details',
                    style: TextStyle(
                      color: Colors.black,
                      fontSize: 24.0,
                    ),
                  ),
                ),
              ),
            ],
          ),
          SizedBox(height: sz.height * 0.3),
        ],
      ),
    );
  }
}

class BooksList extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Container(
            child: Center(
                child: Text(
      'Available books list page',
    ))));
  }
}

class ContactDetails extends StatelessWidget {
  Map user_details;

  ContactDetails({this.user_details});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        child: Center(
          child: Text(
            'Point of Contact\'s contact details page',
          ),
        ),
      ),
    );
  }
}

class PanchayatDetails extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        child: Center(
          child: Text(
            'Panchayat information page',
          ),
        ),
      ),
    );
  }
}
