import 'package:flutter/material.dart';
import 'package:wang/Views/UploadContext.dart';
import 'package:wang/Views/WhatsappConnect.dart';

class MainPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          // Green background on the top 30% of the screen
          Positioned(
            top: 0,
            left: 0,
            right: 0,
            child: Container(
              height: MediaQuery.of(context).size.height * 0.35,
              color: Colors.green,
            ),
          ),
          Column(
            mainAxisAlignment: MainAxisAlignment.start,
            children: <Widget>[
              SizedBox(height: MediaQuery.of(context).size.height * 0.05),
              const Text(
                'Welcome To VAWG -\n Violence Against Women and Girls',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontFamily: 'titleFont',
                  fontSize: 48,
                  fontWeight: FontWeight.w300,
                  color: Colors
                      .white, // Ensuring text is visible on green background
                ),
              ),
              SizedBox(height: 25),
              const Text(
                'To get to work, click on WhatsApp Connect\nIf you want to see the statistics or upload another WhatsApp conversation, click on Statistic Page',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontFamily: 'primeryFont',
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Colors
                      .white, // Ensuring text is visible on green background
                ),
              ),
              Expanded(
                child: Center(
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: <Widget>[
                      Padding(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 50, vertical: 30),
                        // Use SizedBox to wrap the button for full width
                        child: SizedBox(
                          width: 300, // Makes the button stretch
                          child: ElevatedButton(
                            onPressed: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                    builder: (context) => WhatsappConnect()),
                              );
                            },
                            child: Text('WhatsApp Connect',
                                style: TextStyle(fontSize: 20)),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors
                                  .lightGreenAccent, // Light colored button
                              padding: EdgeInsets.symmetric(
                                  vertical:
                                      20), // Increase padding for bigger button
                            ),
                          ),
                        ),
                      ),
                      Padding(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 50, vertical: 10),
                        // Use SizedBox to wrap the button for full width
                        child: SizedBox(
                          width: 300, // Makes the button stretch
                          child: ElevatedButton(
                            onPressed: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                    builder: (context) => UploadContext()),
                              );
                            },
                            child: Text('Upload Context',
                                style: TextStyle(fontSize: 20)),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors
                                  .lightGreenAccent, // Light colored button
                              padding: EdgeInsets.symmetric(
                                  vertical:
                                      20), // Increase padding for bigger button
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
