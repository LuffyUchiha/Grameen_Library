import 'package:flutter/material.dart';

import '../parts.dart';
import '../static_pages.dart';
import '../RolePages/user_page.dart';
import '../RolePages/donor_page.dart';
import '../RolePages/panchayat_page.dart';
import '../RolePages/admin_page.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

http.Client _getClient(){
  return http.Client();
}

class VolunteerForm extends StatefulWidget {
  @override
  _VolunteerFormState createState() => _VolunteerFormState();
}

class _VolunteerFormState extends State<VolunteerForm> {
  String _name;
  String _id;

  GlobalKey<FormState> _formkey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    BoxDecoration _decoration = DecorateField().decoration1();
    return Scaffold(
      body: Center(
        child: Form(
          key: _formkey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Volunteer Register',
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
                        labelText: 'Name',
                      ),
                      validator: (String value) {
                        if (value.isEmpty) {
                          return 'This field cannot be empty';
                        }
                        return null;
                      },
                      onSaved: (String value) {
                        _name = value;
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
                        labelText: 'PMI ID',
                      ),
                      obscureText: true,
                      onSaved: (String value) {
                        _id = value;
                      },
                    ),
                  ),
                  SizedBox(
                    height: MediaQuery.of(context).size.height * 0.01,
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
                        try{
                          await client.post("http://127.0.0.1:5000/login",
                              body : {"user_id": _id,
                                "password": 1})
                              .then((response) {
                            Map<String, dynamic> data = jsonDecode(response.body);
                            print('Howdy, ${data['Name']}, res is ${data['Response']}');
                            res=data['Response'];
                          });
                        }
                        catch(e){
                          print("Failed ->$e");
                        }finally{
                          client.close();
                        }
                        //back_end connect to be inserted
                        print(_id);
                        print(_name);
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
                          Navigator.of(context).push(MaterialPageRoute(
                            builder: (context) => (UsingGrameenLibrary()),
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
    ),
    );
  }
}
