import 'package:flutter/material.dart';

import 'LoginPage.dart';
import 'parts.dart';
import 'static_pages.dart';
import 'RolePages/user_page.dart';
import 'RolePages/donor_page.dart';
import 'RolePages/panchayat_page.dart';
import 'RolePages/admin_page.dart';
import 'FormPages/LoginForm.dart';
import 'FormPages/VolunteerForm.dart';
import 'FormPages/DonorForm.dart';
import 'FormPages/PanchayatForm.dart';
import 'FormPages/UserForm.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() async{
  WidgetsFlutterBinding.ensureInitialized();
  SharedPreferences.setMockInitialValues({});
  SharedPreferences prefs = await SharedPreferences.getInstance();
  bool isLogged = (prefs.getBool('isLogged') ?? false);
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
//      initialRoute: '/',
//      routes:{
//        '/':(context) => LoginPage(),
//        '/register/donor':(context)=>DonorForm(),
//        '/register/volunteer':(context)=>VolunteerForm(),
//        '/register/user':(context)=>userForm(),
//        '/register/panchayat':(context)=>PanchayatForm(),
//        '/login':(context)=>LoginForm()
//      },
      debugShowCheckedModeBanner: false,
//      home: UserPage(),
      home: DonorPage(),
//      home: PanchayatPage(),
    );
  }
}
class LandingPage extends StatefulWidget{
  @override
  _LandingPageState createState() => _LandingPageState();
}
class _LandingPageState extends State<LandingPage> {
  @override
  Widget build(BuildContext context) {
    Size sz = MediaQuery.of(context).size;
    return LoginPage();
  }
}
