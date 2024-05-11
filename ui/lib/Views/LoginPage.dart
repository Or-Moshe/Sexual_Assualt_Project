import 'package:flutter/material.dart';
import 'package:wang/Views/LoginFormPage.dart';
import 'package:wang/Views/MainPage.dart';
import 'package:wang/Views/SignUpPage.dart';

class LoginPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          // Dark green top section
          Container(
            height: MediaQuery.of(context).size.height * 0.35,
            color: const Color.fromARGB(255, 62, 173, 66),
            width: double.infinity,
            child: Center(
              child: const Text(
                'Welcome',
                style: TextStyle(
                    fontFamily: 'titleFont',
                    fontSize: 44,
                    color: Colors.white,
                    fontWeight: FontWeight.w300),
              ),
            ),
          ),
          Expanded(
            child: Center(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: <Widget>[
                    // Use SizedBox for full width buttons
                    SizedBox(
                      width: double
                          .infinity, // Makes the button stretch to max width
                      child: ElevatedButton(
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                                builder: (context) => LoginFormPage()),
                          );
                          // Navigate to Login page (Assuming you have one)
                        },
                        child: Text('Log In', style: TextStyle(fontSize: 20)),
                        style: ElevatedButton.styleFrom(
                          padding: EdgeInsets.symmetric(vertical: 20),
                          shape: RoundedRectangleBorder(
                            borderRadius:
                                BorderRadius.circular(10), // Rounded corners
                          ),
                        ),
                      ),
                    ),
                    SizedBox(height: 20), // Spacing between buttons
                    SizedBox(
                      width: double.infinity, // Full width
                      child: ElevatedButton(
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                                builder: (context) => SignUpPage()),
                          );
                        },
                        child: Text('Sign Up', style: TextStyle(fontSize: 20)),
                        style: ElevatedButton.styleFrom(
                          padding: EdgeInsets.symmetric(vertical: 20),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(10),
                          ),
                        ),
                      ),
                    ),
                    SizedBox(height: 20),
                    SizedBox(
                      width: double.infinity, // Full width
                      child: ElevatedButton(
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(builder: (context) => MainPage()),
                          );
                        },
                        child: Text('Continue as Guest',
                            style: TextStyle(fontSize: 20)),
                        style: ElevatedButton.styleFrom(
                          padding: EdgeInsets.symmetric(vertical: 20),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(10),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
