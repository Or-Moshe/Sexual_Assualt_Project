import 'package:flutter/material.dart';

class UploadContext extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Upload Context'),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              TextField(
                decoration: InputDecoration(
                  hintText: 'Enter your text here Please',
                  border: OutlineInputBorder(),
                ),
                maxLines: 10, // Makes the text field larger
                keyboardType: TextInputType.multiline,
              ),
              SizedBox(
                  height: 20), // Adds space between the text field and button
              ElevatedButton(
                onPressed: () {
                  // Add your onPressed logic here
                },
                child: Text('Send'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
