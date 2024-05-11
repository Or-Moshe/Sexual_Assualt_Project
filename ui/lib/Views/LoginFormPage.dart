import 'package:flutter/material.dart';
// Import necessary for navigating to MainPage or other relevant pages

class LoginFormPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Log in')),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          mainAxisSize: MainAxisSize.min, // Keep the content compact
          children: [
            TextField(
              decoration: InputDecoration(
                labelText: 'Username',
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
            SizedBox(height: 30),
            SizedBox(
              width: double.infinity, // Full-width button
              child: ElevatedButton(
                onPressed: () {
                  // Handle login logic
                },
                child: Text('Log in', style: TextStyle(fontSize: 20)),
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
