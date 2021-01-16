import 'package:flutter/material.dart';
import 'package:grameen_library_front_end/FormPages/LoginForm.dart';
import 'package:grameen_library_front_end/parts.dart';



import 'package:http/http.dart' as http;
import 'dart:convert';

import 'package:shared_preferences/shared_preferences.dart';

import 'FormPages/VolunteerForm.dart';

class LoginPage extends StatefulWidget {
  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  SharedPreferences sharedPreferences;
  String username;
  String id;
  bool isLogged;
  var home;
  @override
  void initState(){
    setData();
  }

  void setData() async{
    sharedPreferences = await SharedPreferences.getInstance();

    setState(() {
      username = sharedPreferences.getString("username") ?? "Error";
      id = sharedPreferences.getString("userid") ?? "Error";
      isLogged= sharedPreferences.getBool("isLogged") ?? false;
      print(username);
      print(id);
      print(isLogged);
      if (isLogged){
        home=VolunteerForm();
      }
      else{
        home=LoginForm();
      }
      print(home);
    });
  }

  void _logout() async {
    sharedPreferences = await SharedPreferences.getInstance();
    sharedPreferences.setBool("isLogged", false);
    Navigator.of(context).pushReplacementNamed('/login');
  }
  Widget build(BuildContext context) {
    Size sz = MediaQuery.of(context).size;
    return Scaffold(
      body: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: <Widget>[
          LeftSide(),
          home==null?Container():home,
          RegisterSide(),
        ],
      ),
    );
  }
}
