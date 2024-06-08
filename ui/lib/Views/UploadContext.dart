import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class UploadContext extends StatefulWidget {
  @override
  _UploadContextState createState() => _UploadContextState();
}

class _UploadContextState extends State<UploadContext> {
  final TextEditingController _controller = TextEditingController();

  Future<String> sendDataToServer(String text, String lang) async {
    try {
      final uri = Uri.http('127.0.0.1:8000', '/analyze_by_vectors', {'text': text, 'lang': lang});
      final response = await http.get(uri, headers: {
        'Content-Type': 'application/json',
      });

      if (response.statusCode == 200) {
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
                  String response = await sendDataToServer(_controller.text, 'en'); // Change 'en' to the desired language
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
