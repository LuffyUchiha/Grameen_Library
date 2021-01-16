import 'package:flutter/material.dart';
import 'package:grameen_library_front_end/FormPages/LoginForm.dart';

import '../LoginPage.dart';
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

class DonorForm extends StatefulWidget {
  @override
  _DonorFormState createState() => _DonorFormState();
}

class _DonorFormState extends State<DonorForm> {
  String _name;
  String _email;
  String _phone;
  String _password;
  String _pass_val;

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
                'Donor Register',
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
                        labelText: 'Email',
                      ),
                      validator: (String value) {
                        if (value.isEmpty) {
                          return 'This field cannot be empty';
                        }
                        if(!value.contains('@') || !value.contains('.')){
                          return 'Please enter a valid email';
                        }
                        return null;
                      },
                      onSaved: (String value) {
                        _email = value;
                      },
                    ),
                  ),
                  SizedBox(
                    height: MediaQuery.of(context).size.height * 0.03,
                  ),
                  Container(
                    decoration: _decoration,
                    constraints: BoxConstraints(
                      maxHeight: MediaQuery.of(context).size.height * 0.1,
                      maxWidth: MediaQuery.of(context).size.width * 0.25,
                    ),
                    child: TextFormField(
                      decoration: InputDecoration(
                        border: OutlineInputBorder(),
                        labelText: 'Phone',
                      ),
                      validator: (String value) {
                        if (value.isEmpty ) {
                          return 'This field cannot be empty';
                        }
                        if( value.length!=10){
                          return 'Please enter a valid mobile number';
                        }
                        return null;
                      },
                      onSaved: (String value) {
                        _phone = value;
                      },
                    ),
                  ),
                  SizedBox(
                    height: MediaQuery.of(context).size.height * 0.03,
                  ),
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
                      validator: (String value) {
                        _pass_val=value;
                        if (value.isEmpty) {
                          return 'This field cannot be empty';
                        }
                        return null;
                      },
                      obscureText: true,
                      onSaved: (String value) {
                        _password = value;
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
                        labelText: 'Confirm Password',
                      ),
                      obscureText: true,
                      validator: (String value) {
                        if (value.isEmpty) {
                          return 'This field cannot be empty';
                        }
                        if (value.compareTo(_pass_val)!=0){
                          return 'Passwords are not matching';
                        }
                        return null;
                      },
                    ),
                  ),
                  SizedBox(height: MediaQuery.of(context).size.height * 0.03),
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
                          await client.post("http://127.0.0.1:5000/register/donor",
                              body : {"Name":_name,"Email":_email,"Phone":_phone,"Password":_password})
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
                        print(_name);
                        Navigator.of(context).push(MaterialPageRoute(
                          builder: (context) => (LoginPage()),
                        ));
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
