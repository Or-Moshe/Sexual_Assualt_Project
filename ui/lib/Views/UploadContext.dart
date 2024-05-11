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
      // Replace 'http://example.com/api' with your actual URL
      final response = await http.post(
        Uri.parse('http://127.0.0.1:8000'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization':
              'Bearer your_api_token', // Include this only if needed
        },
        body: jsonEncode({'text': text}),
      );

      if (response.statusCode == 200) {
        // Assuming the server returns a string within a JSON object
        return jsonDecode(response.body)['data'];
      } else {
        throw Exception('Failed to load data');
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
