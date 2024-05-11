import 'package:flutter/material.dart';
// Ensure you have the appropriate navigation imports if needed

class SignUpPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Sign Up'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisSize: MainAxisSize.min, // To make content more compact
          children: <Widget>[
            TextField(
              decoration: InputDecoration(
                labelText: 'Name',
                border: OutlineInputBorder(), // Adds border around TextField
                contentPadding: EdgeInsets.symmetric(
                    horizontal: 10,
                    vertical: 15), // Better padding inside TextField
              ),
            ),
            SizedBox(height: 16),
            TextField(
              decoration: InputDecoration(
                labelText: 'Email',
                border: OutlineInputBorder(),
                contentPadding:
                    EdgeInsets.symmetric(horizontal: 10, vertical: 15),
              ),
            ),
            SizedBox(height: 16),
            TextField(
              decoration: InputDecoration(
                labelText: 'Password',
                border: OutlineInputBorder(),
                contentPadding:
                    EdgeInsets.symmetric(horizontal: 10, vertical: 15),
              ),
              obscureText: true,
            ),
            SizedBox(height: 16),
            TextField(
              decoration: InputDecoration(
                labelText: 'Confirm Password',
                border: OutlineInputBorder(),
                contentPadding:
                    EdgeInsets.symmetric(horizontal: 10, vertical: 15),
              ),
              obscureText: true,
            ),
            SizedBox(height: 30),
            SizedBox(
              width: double.infinity, // Full-width button
              child: ElevatedButton(
                onPressed: () {
                  // Implement sign-up logic
                },
                child: Text('Sign Up', style: TextStyle(fontSize: 20)),
                style: ElevatedButton.styleFrom(
                  padding: EdgeInsets.symmetric(vertical: 20), // Taller button
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
