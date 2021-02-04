import 'dart:collection';
import 'dart:convert';
import 'dart:io';
import 'package:flutter/cupertino.dart';
import 'package:grameen_library_front_end/LoginPage.dart';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:syncfusion_flutter_charts/charts.dart';

import 'package:grameen_library_front_end/static_pages.dart';
import 'package:grameen_library_front_end/parts.dart';

http.Client _getClient() {
  return http.Client();
}

class DonorPage extends StatelessWidget {
  String username;
  String id;
  int num_of_books;
  bool isLogged;

  DonorPage() {
    this.getDetails();
  }

  Future<void> getDetails() async {
    SharedPreferences sharedPreferences = await SharedPreferences.getInstance();
    this.username = sharedPreferences.getString("username") ?? "Error";
    this.id = sharedPreferences.getString("userid") ?? "Error";
    isLogged = sharedPreferences.getBool("isLogged") ?? false;
    num_of_books = sharedPreferences.getInt("book_count");
    print("isLogged : " + sharedPreferences.getBool("isLogged").toString());
  }

  @override
  Widget build(BuildContext context) {
    Size sz = MediaQuery.of(context).size;
    return Scaffold(
      body: Container(
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            LeftSide(),
            Content(
              donor_id: this.id,
              num_of_books: this.num_of_books,
            ),
            RightSide(username: this.username),
          ],
        ),
      ),
    );
  }
}

class Content extends StatelessWidget {
  String donor_id;
  int num_of_books;

  Content({this.donor_id, this.num_of_books});

  @override
  Widget build(BuildContext context) {
    Size sz = MediaQuery.of(context).size;
    return Container(
      margin: EdgeInsets.symmetric(horizontal: sz.width * 0.025),
      child: Container(
        width: sz.width * 0.33,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Donor Dashboard (Default)',
                  style: TextStyle(
                    color: Colors.black,
                    fontSize: 28.0,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                Row(
                  children: [
                    Text('Donor ID : '),
                    Text(
                      '$donor_id',
                      style: TextStyle(
                        color: Colors.black,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    SizedBox(
                      width: sz.width * 0.03,
                    ),
                    Text('Number of books donated : '),
                    Text(
                      '$num_of_books',
                      style: TextStyle(
                        color: Colors.black,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ],
            ),
            DashBoard(),
          ],
        ),
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
      alignment: Alignment.center,
      width: sz.width * 0.33,
      margin: EdgeInsets.symmetric(horizontal: sz.width * 0.025),
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
                      builder: (context) => BookDetails(),
                    ),
                  );
                },
                child: Container(
                  child: Text('Show Book\'s Usage'),
                ),
              ),
              SizedBox(height: MediaQuery.of(context).size.height * 0.03),
              InkWell(
                onTap: () {
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => _DonateBooks(),
                    ),
                  );
                },
                child: Container(
                  child: Text('Donate Books'),
                ),
              ),
              SizedBox(height: MediaQuery.of(context).size.height * 0.03),
              InkWell(
                onTap: () {
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => ContactDetails(),
                    ),
                  );
                },
                child: Container(
                  child: Text('Donor User Details'),
                ),
              ),
              SizedBox(height: MediaQuery.of(context).size.height * 0.03),
              InkWell(
                onTap: () {
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => ChangeUserDetails(),
                    ),
                  );
                },
                child: Container(
                  child: Text('Change Contact Details'),
                ),
              ),
              SizedBox(
                height: MediaQuery.of(context).size.height * 0.15,
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class BookDetails extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    //TODO show the books the donor has donated like shown in the UI process flow
    return Scaffold(
      body: Center(
        child: Container(
          child: Text('Show book statistics here'),
        ),
      ),
    );
  }
}

class _DonateBooks extends StatefulWidget {

//  String book_name;
//
//  String ISBN;
//
//  String author_name;
//
//  String category;
//
  String id;

  bool isLogged;

  _DonateBooks() {
    this.getDetails();
  }

  Future<void> getDetails() async {
    SharedPreferences sharedPreferences = await SharedPreferences.getInstance();
    this.id = sharedPreferences.getString("userid") ?? "Error";
    isLogged = sharedPreferences.getBool("isLogged") ?? false;
    print("isLogged : " + sharedPreferences.getBool("isLogged").toString());
  }

  @override
  __DonateBooksState createState() => __DonateBooksState();
}

class __DonateBooksState extends State<_DonateBooks> {
  GlobalKey<FormState> formkey = GlobalKey<FormState>();

  String book_name;

  String ISBN;

  String author_name;

  String category;

  String id;

  bool isLogged;

  int _num;

  __DonateBooksState(
//      {this.book_name,
//      this.formkey,
//      this.id,
//      this.author_name,
//      this.category,
//      this.ISBN,
//      this.isLogged}
      );

  Widget _formbook(int index) {
    return Container(
      child: TextFormField(
        decoration: InputDecoration(
          border: OutlineInputBorder(),
          labelText: 'Book Number $index',
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    //TODO develop a donate form, not sure about the nuances so left blank
    BoxDecoration _decoration = DecorateField().decoration1();
    return Scaffold(
      body: SingleChildScrollView(
        child: Center(
          child: Container(
            padding:
                EdgeInsets.only(top: MediaQuery.of(context).size.height * 0.1),
            constraints: BoxConstraints(
              maxWidth: MediaQuery.of(context).size.width * 0.5,
            ),
            child: Column(
              children: [
                Container(
                  decoration: _decoration,
                  child: TextFormField(
                    decoration: InputDecoration(
                      border: OutlineInputBorder(),
                      labelText: 'Number of Books',
                    ),
                    validator: (String value) {
                      try {
                        var i = int.parse(value);
                        return null;
                      } on FormatException {
                        return "Enter an integer";
                      }
                    },
                    autovalidateMode: AutovalidateMode.always,
                    onChanged: (String val) {
                      setState(() {
                        _num = int.parse(val);
                      });
                    },
                  ),
                ),
                for (int i = 0; i < _num; i++) _formbook(i),
              ],
            ),
          ),
        ),
      ),
    );
//    return Container(
//      child: Form(
//        key: _formkey,
//        child: Column(
//            mainAxisAlignment: MainAxisAlignment.center,
//            crossAxisAlignment: CrossAxisAlignment.start,
//            children: <Widget>[
//              Text(
//                'Donate Books',
//                style: TextStyle(
//                  color: Colors.black,
//                  fontSize: 30.0,
//                  fontWeight: FontWeight.w500,
//                ),
//              ),
//              SizedBox(height: MediaQuery.of(context).size.height * 0.03),
//              Column(
//                crossAxisAlignment: CrossAxisAlignment.center,
//                children: <Widget>[
//                  Container(
//                    decoration: _decoration,
//                    constraints: BoxConstraints(
//                      maxHeight: MediaQuery.of(context).size.height * 0.1,
//                      maxWidth: MediaQuery.of(context).size.width * 0.25,
//                    ),
//                    child: TextFormField(
//                      decoration: InputDecoration(
//                        border: OutlineInputBorder(),
//                        labelText: 'Book Name',
//                      ),
//                      onSaved: (String value) {
//                        book_name = value;
//                      },
//                    ),
//                  ),
//                  SizedBox(height: MediaQuery.of(context).size.height * 0.03),
//                  Container(
//                    decoration: _decoration,
//                    constraints: BoxConstraints(
//                      maxHeight: MediaQuery.of(context).size.height * 0.1,
//                      maxWidth: MediaQuery.of(context).size.width * 0.25,
//                    ),
//                    child: TextFormField(
//                      decoration: InputDecoration(
//                        border: OutlineInputBorder(),
//                        labelText: 'ISBN',
//                      ),
//                      onSaved: (String value) {
//                        ISBN = value;
//                      },
//                    ),
//                  ),
//                  SizedBox(
//                    height: MediaQuery.of(context).size.height * 0.01,
//                  ),
//                  Container(
//                    decoration: _decoration,
//                    constraints: BoxConstraints(
//                      maxHeight: MediaQuery.of(context).size.height * 0.1,
//                      maxWidth: MediaQuery.of(context).size.width * 0.25,
//                    ),
//                    child: TextFormField(
//                      decoration: InputDecoration(
//                        border: OutlineInputBorder(),
//                        labelText: 'Author Name',
//                      ),
//                      onSaved: (String value) {
//                        author_name = value;
//                      },
//                    ),
//                  ),
//                  SizedBox(
//                    height: MediaQuery.of(context).size.height * 0.03,
//                  ),
//                  Container(
//                    decoration: _decoration,
//                    constraints: BoxConstraints(
//                      maxHeight: MediaQuery.of(context).size.height * 0.1,
//                      maxWidth: MediaQuery.of(context).size.width * 0.25,
//                    ),
//                    child: TextFormField(
//                      decoration: InputDecoration(
//                        border: OutlineInputBorder(),
//                        labelText: 'Category',
//                      ),
//                      onSaved: (String value) {
//                        category = value;
//                      },
//                    ),
//                  ),
//                  SizedBox(
//                    height: MediaQuery.of(context).size.height * 0.03,
//                  ),
//                  Container(
//                    constraints: BoxConstraints(
//                      minWidth: 100,
//                      minHeight: 40,
//                    ),
//                    child: RaisedButton(
//                      color: Colors.lightBlue[600],
//                      onPressed: () async {
//                        if (!_formkey.currentState.validate()) return;
//                        _formkey.currentState.save();
//                        var client = _getClient();
//                        var username="";
//                        try{
//                          await client.post("http://127.0.0.1:5000/donate_book",
//                              body : {"book_name":book_name,
//                                "id":id,
//                                "ISBN":ISBN,
//                                "author_name":author_name,
//                                "category": category})
//                              .then((response) {
//                            Map<String, dynamic> data = jsonDecode(response.body);
//                          });
//                        }
//                        catch(e){
//                          print("Failed ->$e");
//                        }finally{
//                          client.close();
//                        }
/////////////////////////////////////////////////////////////////////////////////////////////////
    //back_end connect
/////////////////////////////////////////////////////////////////////////////////////////////////
//                        print(_id);
//                        print(_password);
//                        if(res!=1){
//                          await showDialog(
//                            context: context,
//                            builder: (context) => new AlertDialog(
//                              title: new Text('Wrong UserID/Password'),
//                              content: Text(
//                                  'Please try again.'),
//                              actions: <Widget>[
//                                new FlatButton(
//                                  onPressed: () {
//                                    Navigator.of(context)
//                                        .pop(); // dismisses only the dialog and returns nothing
//                                  },
//                                  child: new Text('OK'),
//                                ),
//                              ],
//                            ),
//                          );
//                        }
//                        else{
//                          sharedPreferences = await SharedPreferences.getInstance();
//                          sharedPreferences.setBool("isLogged", true);
//                          sharedPreferences.setString("username", username);
//                          sharedPreferences.setString("userid", _id);
//                          sharedPreferences.setString("role", role);
//                          print("isLogged : " + sharedPreferences.getBool("isLogged").toString());
//                          var redir;
//                          if(role=='user'){
//                            redir=UserPage();
//                          }
//                          else if(role=='donor'){
//                            var client = _getClient();
//                            try{
//                              await client.post("http://127.0.0.1:5000/get_num",
//                                  body : {"user_id":_id})
//                                  .then((response) {
//                                Map<String, dynamic> data = jsonDecode(response.body);
//                                sharedPreferences.setInt("book_count", data['Num']);;
//                              });
//                            }
//                            catch(e){
//                              print("Failed ->$e");
//                            }finally{
//                              client.close();
//                            }
//                            redir=DonorPage();
//                          }
//                          else if(role=='panchayat'){
//                            redir=PanchayatPage();
//                          }
//                          else if(role=='admin'){
//
//                          }
//                          else{
//
//                          }
//                          Navigator.of(context).push(MaterialPageRoute(
//                            builder: (context) => (redir),
//                          ));
//                        }
//                      },
//                      child: Text('Submit'),
//                    ),
//                  ),
//                ],
//              )
//            ]),
//      ),
//    );
  }
}

class DashBoard extends StatelessWidget {
  Map donor_data;

  DashBoard({
    this.donor_data,
  });

  @override
  Widget build(BuildContext context) {
    if (donor_data == null) {
      donor_data = {
        'joining date': DateTime.utc(2019, 5, 4),
        'donated books': {
          DateTime.utc(2019, 6, 12, 23, 14, 23),
          DateTime.utc(2019, 6, 13, 23, 14, 23),
          DateTime.utc(2019, 6, 14, 23, 14, 23),
          DateTime.utc(2019, 6, 15, 23, 14, 23),
          DateTime.utc(2019, 6, 16, 23, 14, 23),
        }
      };
    }
    HashSet<DateTime> donations = donor_data['donated books'];
    List<List<int>> dons = new List();
    donations.forEach((element) {
      dons.add([element.year, element.month]);
    });
    List<int> join_date = [
      donor_data['joining date'].year,
      donor_data['joining date'].month
    ];
    print(dons);
    print(join_date);
    return Container(
      child: SfCartesianChart(
          primaryXAxis: CategoryAxis(),
          title: ChartTitle(text: 'Donations by you'), //Chart title.
          tooltipBehavior: TooltipBehavior(
            enable: true,
          ),
          series: <LineSeries<int, String>>[
            LineSeries<int, String>(
                dataSource: [1, 2, 3, 4],
                xValueMapper: (int x, _) {
                  return x.toString();
                },
                yValueMapper: (int x, _) => x,
                dataLabelSettings: DataLabelSettings(
                    isVisible: true) // Enables the data label.
                )
          ]),
    );
  }
}

class ContactDetails extends StatelessWidget {
  Map user_details;

  ContactDetails({this.user_details});

  @override
  Widget build(BuildContext context) {
    //TODO get the donor details from the login page give them as an input to this widget
    //TODO display the donor details in a neat and minimalistic fashion
    return Scaffold(
      body: Center(
        child: Container(
          child: Text('Show donor contact details page'),
        ),
      ),
    );
  }
}

class ChangeUserDetails extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    //TODO come up with a way to let the user change his details/credentials
    return Scaffold(
      body: Center(
        child: Container(
          child: Text('Change donor contact details page'),
        ),
      ),
    );
  }
}
