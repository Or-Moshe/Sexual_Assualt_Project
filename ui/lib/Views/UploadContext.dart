import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class UploadContext extends StatefulWidget {
  @override
  _UploadContextState createState() => _UploadContextState();
}

class _UploadContextState extends State<UploadContext> {
  final TextEditingController _controller = TextEditingController();

  Future<String> sendDataToServer(String text) async {
    try {
      final response = await http.post(
        Uri.parse(
            'http://127.0.0.1:8000/analyze'), // Updated to the correct API endpoint
        headers: {
          'Content-Type': 'application/json',
          // Remove the Authorization header if your API doesn't require it
        },
        body: jsonEncode({'text': text}),
      );

      if (response.statusCode == 200) {
        // Assuming the server returns data directly without a 'data' key
        return jsonDecode(response.body).toString();
      } else {
        return 'Failed to load data: Status code ${response.statusCode}';
      }
    } catch (e) {
      return 'Failed to send data: $e';
    }
  }

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
                controller: _controller,
                decoration: InputDecoration(
                  hintText: 'Enter your text here Please',
                  border: OutlineInputBorder(),
                ),
                maxLines: 10,
              ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: () async {
                  String response = await sendDataToServer(_controller.text);
                  showDialog(
                    context: context,
                    builder: (context) => AlertDialog(
                      title: Text('Response from Server'),
                      content: Text(response),
                      actions: <Widget>[
                        TextButton(
                          onPressed: () {
                            Navigator.of(context).pop();
                          },
                          child: Text('OK'),
                        ),
                      ],
                    ),
                  );
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
