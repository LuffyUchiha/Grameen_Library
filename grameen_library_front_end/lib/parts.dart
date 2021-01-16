import 'package:flutter/material.dart';

import 'static_pages.dart';
import 'FormPages/LoginForm.dart';
import 'FormPages/VolunteerForm.dart';
import 'FormPages/DonorForm.dart';
import 'FormPages/PanchayatForm.dart';
import 'FormPages/UserForm.dart';

class DecorateField {
  BoxDecoration decoration1() => BoxDecoration(
        gradient: LinearGradient(
          colors: [Colors.white, Colors.blueAccent, Colors.blue[800]],
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
        ),
      );

  BoxDecoration decoration2() => BoxDecoration(
        gradient: LinearGradient(
          colors: [Colors.white, Colors.blueAccent],
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
        ),
      );
  BoxDecoration decoration3(Size size) => BoxDecoration(
    border: Border.all(
      color: Colors.red,
      width: size.height/1000 + size.width/1000,
    ),
    gradient: LinearGradient(
      colors: [Colors.white, Colors.blueAccent, Colors.blue[800]],
      begin: Alignment.topCenter,
      end: Alignment.bottomCenter,
    ),
  );
}


class LeftSide extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    Size sz = MediaQuery
        .of(context)
        .size;
    return Container(
      alignment: Alignment.centerLeft,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget>[
          Container(
            constraints: BoxConstraints(
              minHeight: sz.height / 20,
              minWidth: sz.width / 10,
            ),
            margin: EdgeInsets.symmetric(
                vertical: sz.height / 40, horizontal: sz.width / 40),
            child: InkWell(
              splashColor: Colors.blueAccent,
              child: Center(
                child: Text(
                  'About Grameen Library',
                  style: TextStyle(
                    color: Colors.black,
                    fontWeight: FontWeight.w500,
                    fontSize: 24,
                  ),
                ),
              ),
              onTap: () {
                Navigator.of(context).push(
                  MaterialPageRoute(
                    builder: (context) => AboutGrameenLibrary(),
                  ),
                );
              },
            ),
          ),
          Container(
            constraints: BoxConstraints(
              minHeight: sz.height / 20,
              minWidth: sz.width / 10,
            ),
            margin: EdgeInsets.symmetric(
                vertical: sz.height / 40, horizontal: sz.width / 40),
            child: InkWell(
              splashColor: Colors.blueAccent,
              child: Center(
                child: Text(
                  'How To Donate Books',
                  style: TextStyle(
                    color: Colors.black,
                    fontWeight: FontWeight.w500,
                    fontSize: 24,
                  ),
                ),
              ),
              onTap: () {
                Navigator.of(context).push(
                  MaterialPageRoute(
                    builder: (context) => DonateBooks(),
                  ),
                );
              },
            ),
          ),
          Container(
            constraints: BoxConstraints(
              minHeight: sz.height / 20,
              minWidth: sz.width / 10,
            ),
            margin: EdgeInsets.symmetric(
                vertical: sz.height / 40, horizontal: sz.width / 40),
            child: InkWell(
              splashColor: Colors.blueAccent,
              child: Center(
                child: Text(
                  'Using The Library',
                  style: TextStyle(
                    color: Colors.black,
                    fontWeight: FontWeight.w500,
                    fontSize: 24,
                  ),
                ),
              ),
              onTap: () {
                Navigator.of(context).push(
                  MaterialPageRoute(
                    builder: (context) => UsingGrameenLibrary(),
                  ),
                );
              },
            ),
          )
        ],
      ),
    );
  }
}



class RegisterSide extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    Size sz = MediaQuery
        .of(context)
        .size;
    return Container(
      alignment: Alignment.centerLeft,
      child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: <Widget>[
              Text(
                'Registration',
                style: TextStyle(
                  color: Colors.black,
                  fontWeight: FontWeight.w500,
                  fontSize: 26,
                ),
              ),
              Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  Container(
                    constraints: BoxConstraints(
                      minHeight: sz.height / 20,
                      minWidth: sz.width / 10,
                    ),
                    margin: EdgeInsets.symmetric(
                      vertical: sz.height * 0.01,
                      horizontal: sz.width * 0.025,
                    ),
                    child: InkWell(
                      splashColor: Colors.blueAccent,
                      child: Center(
                        child: Text(
                          'Volunteer',
                          style: TextStyle(
                            color: Colors.black,
                            fontWeight: FontWeight.w500,
                            fontSize: 24,
                          ),
                        ),
                      ),
                      onTap: () {
                        Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (context) => VolunteerForm(),
                          ),
                        );
                      },
                    ),
                  ),
                  Container(
                    constraints: BoxConstraints(
                      minHeight: sz.height / 20,
                      minWidth: sz.width / 10,
                    ),
                    margin: EdgeInsets.symmetric(
                        vertical: sz.height / 100, horizontal: sz.width / 40),
                    child: InkWell(
                      splashColor: Colors.blueAccent,
                      child: Center(
                        child: Text(
                          'Donor',
                          style: TextStyle(
                            color: Colors.black,
                            fontWeight: FontWeight.w500,
                            fontSize: 24,
                          ),
                        ),
                      ),
                      onTap: () {
                        Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (context) => DonorForm(),
                          ),
                        );
                      },
                    ),
                  ),
                  Container(
                    constraints: BoxConstraints(
                      minHeight: sz.height / 20,
                      minWidth: sz.width / 10,
                    ),
                    margin: EdgeInsets.symmetric(
                        vertical: sz.height / 100, horizontal: sz.width / 40),
                    child: InkWell(
                      splashColor: Colors.blueAccent,
                      child: Center(
                        child: Text(
                          'User',
                          style: TextStyle(
                            color: Colors.black,
                            fontWeight: FontWeight.w500,
                            fontSize: 24,
                          ),
                        ),
                      ),
                      onTap: () {
                        Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (context) => userForm(),
                          ),
                        );
                      },
                    ),
                  ),
                  Container(
                    constraints: BoxConstraints(
                      minHeight: sz.height / 20,
                      minWidth: sz.width / 10,
                    ),
                    margin: EdgeInsets.symmetric(
                        vertical: sz.height / 100, horizontal: sz.width / 40),
                    child: InkWell(
                      splashColor: Colors.blueAccent,
                      child: Center(
                        child: Text(
                          'Panchayat',
                          style: TextStyle(
                            color: Colors.black,
                            fontWeight: FontWeight.w500,
                            fontSize: 24,
                          ),
                        ),
                      ),
                      onTap: () {
                        Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (context) => PanchayatForm(),
                          ),
                        );
                      },
                    ),
                  ),
                ],
              ),
            ],
          ),
    );
  }
}