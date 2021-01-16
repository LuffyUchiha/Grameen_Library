import 'package:flutter/material.dart';



class AboutGrameenLibrary extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Text(
          'Hi this is the page in which the information regarding the grameen '
          'library will be shown',
          style: TextStyle(
            color: Colors.black,
            fontSize: 24.0,
          ),
        ),
      ),
    );
  }
}

class DonateBooks extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Text(
          'This is the page in which the process of donating the books will be specified',
          style: TextStyle(
            color: Colors.black,
            fontSize: 24.0,
          ),
        ),
      ),
    );
  }
}

class UsingGrameenLibrary extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Text(
          'This is the page in which the process of using the Grameen Library portal will be described',
          style: TextStyle(
            color: Colors.black,
            fontSize: 24.0,
          ),
        ),
      ),
    );
  }
}

class ForgotUsernamePassword extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        child: Center(child: Text('Forgot Username/Password')),
      ),
    );
  }
}
