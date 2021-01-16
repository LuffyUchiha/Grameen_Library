import 'package:flutter/material.dart';

import '../parts.dart';
import '../static_pages.dart';
import '../RolePages/user_page.dart';
import '../RolePages/donor_page.dart';
import '../RolePages/panchayat_page.dart';
import '../RolePages/admin_page.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

http.Client _getClient(){
  return http.Client();
}

class LoginForm extends StatefulWidget {
  @override
  _LoginFormState createState() => _LoginFormState();
}

class _LoginFormState extends State<LoginForm> {
  String _id;
  String _password;
  SharedPreferences sharedPreferences;

  GlobalKey<FormState> _formkey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    BoxDecoration _decoration = DecorateField().decoration1();

    return Container(
      child: Form(
        key: _formkey,
        child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: <Widget>[
              Text(
                'Login',
                style: TextStyle(
                  color: Colors.black,
                  fontSize: 30.0,
                  fontWeight: FontWeight.w500,
                ),
              ),
              SizedBox(height: MediaQuery.of(context).size.height * 0.03),
              Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                children: <Widget>[
                  Container(
                    decoration: _decoration,
                    constraints: BoxConstraints(
                      maxHeight: MediaQuery.of(context).size.height * 0.1,
                      maxWidth: MediaQuery.of(context).size.width * 0.25,
                    ),
                    child: TextFormField(
                      decoration: InputDecoration(
                        border: OutlineInputBorder(),
                        labelText: 'User ID',
                      ),
                      validator: (String value) {
                        if (value.isEmpty) {
                          return 'This field cannot be empty';
                        }
                        return null;
                      },
                      onSaved: (String value) {
                        _id = value;
                      },
                    ),
                  ),
                  SizedBox(height: MediaQuery.of(context).size.height * 0.03),
                  Container(
                    decoration: _decoration,
                    constraints: BoxConstraints(
                      maxHeight: MediaQuery.of(context).size.height * 0.1,
                      maxWidth: MediaQuery.of(context).size.width * 0.25,
                    ),
                    child: TextFormField(
                      decoration: InputDecoration(
                        border: OutlineInputBorder(),
                        labelText: 'Password',
                      ),
                      obscureText: true,
                      validator: (String value) {
                        if (value.isEmpty) {
                          return 'This field cannot be empty';
                        }
                      },
                      onSaved: (String value) {
                        _password = value;
                      },
                    ),
                  ),
                  SizedBox(
                    height: MediaQuery.of(context).size.height * 0.01,
                  ),
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      InkWell(
                        child: Text(
                          'Forgot Password?',
                          style: TextStyle(
                            color: Colors.blue[800],
                            fontSize: 20.0,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        onTap: () {
                          Navigator.of(context).push(MaterialPageRoute(
                            builder: (context) => ForgotUsernamePassword(),
                          ));
                        },
                      ),
                      SizedBox(
                        height: MediaQuery.of(context).size.height * 0.01,
                      ),
                      InkWell(
                        child: Text(
                          'Forgot User ID?',
                          style: TextStyle(
                            color: Colors.blue[800],
                            fontSize: 20.0,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        onTap: () {
                          Navigator.of(context).push(MaterialPageRoute(
                            builder: (context) => ForgotUsernamePassword(),
                          ));
                        },
                      ),
                    ],
                  ),
                  SizedBox(
                    height: MediaQuery.of(context).size.height * 0.03,
                  ),
                  Container(
                    constraints: BoxConstraints(
                      minWidth: 100,
                      minHeight: 40,
                    ),
                    child: RaisedButton(
                      color: Colors.lightBlue[600],
                      onPressed: () async {
                        if (!_formkey.currentState.validate()) return;
                        _formkey.currentState.save();
                        var client = _getClient();
                        var res=0;
                        var username="";
                        var role;
                        try{
                          await client.post("http://127.0.0.1:5000/login",
                              body : {"user_id": _id,
                                "password": _password})
                              .then((response) {
                            Map<String, dynamic> data = jsonDecode(response.body);
                            print('Howdy, ${data['Name']}, res is ${data['Response']}');
                            res=data['Response'];
                            role=data['Role'];
                            if (res==1) {
                              username = data['Name'];
                            }
                          });
                        }
                        catch(e){
                          print("Failed ->$e");
                        }finally{
                          client.close();
                        }
                        //back_end connect to be inserted
                        print(_id);
                        print(_password);
                        if(res!=1){
                          await showDialog(
                            context: context,
                            builder: (context) => new AlertDialog(
                              title: new Text('Wrong UserID/Password'),
                              content: Text(
                                  'Please try again.'),
                              actions: <Widget>[
                                new FlatButton(
                                  onPressed: () {
                                    Navigator.of(context)
                                        .pop(); // dismisses only the dialog and returns nothing
                                  },
                                  child: new Text('OK'),
                                ),
                              ],
                            ),
                          );
                        }
                        else{
                          sharedPreferences = await SharedPreferences.getInstance();
                          sharedPreferences.setBool("isLogged", true);
                          sharedPreferences.setString("username", username);
                          sharedPreferences.setString("userid", _id);
                          sharedPreferences.setString("role", role);
                          var redir;
                          if(role=='user'){
                            redir=UserPage();
                          }
                          else if(role=='donor'){
                            redir=DonorPage();
                          }
                          else if(role=='panchayat'){
                            redir=PanchayatPage();
                          }
                          else if(role=='admin'){

                          }
                          else{

                          }
                          Navigator.of(context).push(MaterialPageRoute(
                            builder: (context) => (redir),
                          ));
                        }
                      },
                      child: Text('Submit'),
                    ),
                  ),
                ],
              )
            ]),
      ),
    );
  }
}
