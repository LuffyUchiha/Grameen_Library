import 'package:flutter/material.dart';

import 'package:grameen_library_front_end/static_pages.dart';
import 'package:grameen_library_front_end/parts.dart';

class DonorPage extends StatelessWidget {
  String username;
  String donor_id;
  int num_of_books;

  DonorPage(
      {this.username = 'DefaultDonor',
      this.donor_id = 'xxxx',
      this.num_of_books = 0});

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
              donor_id: this.donor_id,
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
            Container(
              color: Colors.orangeAccent,
              constraints: BoxConstraints(
                minWidth: sz.width * 0.4,
                minHeight: sz.height * 0.4,
              ),
            ),
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
                      builder: (context) => DonateBooks(),
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
              SizedBox(height: MediaQuery.of(context).size.height * 0.15,),
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

class DonateBooks extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    //TODO develop a donate form, not sure about the nuances so left blank
    return Container();
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
