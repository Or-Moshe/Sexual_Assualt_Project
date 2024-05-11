import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:wang/Views/UploadContext.dart';

class StatisticsPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Statistics Page'),
      ),
      body: Column(
        children: [
          Expanded(
            flex: 8, // Charts take 80% of the height
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Row(
                children: [
                  Expanded(
                    child: LineChart(
                      LineChartData(
                        gridData: FlGridData(show: false),
                        titlesData: FlTitlesData(show: false),
                        borderData: FlBorderData(show: false),
                        lineBarsData: [
                          LineChartBarData(
                            spots: [
                              FlSpot(0, 1),
                              FlSpot(1, 2),
                              FlSpot(2, 3),
                              FlSpot(3, 5),
                              FlSpot(4, 7),
                              FlSpot(5, 5),
                              FlSpot(6, 3),
                              FlSpot(7, 2),
                              FlSpot(8, 1),
                            ],
                            isCurved: true,
                            color: Colors.red,
                            barWidth: 5,
                            isStrokeCapRound: true,
                            dotData: FlDotData(show: false),
                            belowBarData: BarAreaData(show: false),
                          ),
                          LineChartBarData(
                            spots: [
                              FlSpot(2, 1),
                              FlSpot(3, 2),
                              FlSpot(4, 3),
                              FlSpot(5, 5),
                              FlSpot(6, 7),
                              FlSpot(7, 5),
                              FlSpot(8, 3),
                              FlSpot(9, 2),
                              FlSpot(10, 1),
                            ],
                            isCurved: true,
                            color: Colors.blue,
                            barWidth: 5,
                            isStrokeCapRound: true,
                            dotData: FlDotData(show: false),
                            belowBarData: BarAreaData(show: false),
                          ),
                        ],
                      ),
                    ),
                  ),
                  Expanded(
                    child: BarChart(
                      BarChartData(
                        alignment: BarChartAlignment.spaceAround,
                        maxY: 20,
                        barTouchData: BarTouchData(enabled: false),
                        titlesData: FlTitlesData(show: false),
                        borderData: FlBorderData(show: false),
                        barGroups: [
                          BarChartGroupData(
                            x: 0,
                            barRods: [
                              BarChartRodData(toY: 8, color: Colors.lightBlue),
                            ],
                            showingTooltipIndicators: [0],
                          ),
                          BarChartGroupData(
                            x: 1,
                            barRods: [
                              BarChartRodData(toY: 10, color: Colors.lightBlue),
                            ],
                            showingTooltipIndicators: [0],
                          ),
                          BarChartGroupData(
                            x: 2,
                            barRods: [
                              BarChartRodData(toY: 14, color: Colors.lightBlue),
                            ],
                            showingTooltipIndicators: [0],
                          ),
                          BarChartGroupData(
                            x: 3,
                            barRods: [
                              BarChartRodData(toY: 15, color: Colors.lightBlue),
                            ],
                            showingTooltipIndicators: [0],
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
          Expanded(
            flex: 2, // Button takes the remaining 20% of the height
            child: Center(
              child: SizedBox(
                width: 350,
                height: 50,
                child: ElevatedButton(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => UploadContext()),
                    );
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.lightBlueAccent,
                    // If using onPrimary for text color, ensure background is dark enough for contrast
                    // onPrimary: Colors.white,
                  ),
                  child: const Text(
                    'Upload New Conversation',
                    style: TextStyle(
                      fontSize: 22,
                      color: Colors.white, // Specify the text color here
                    ),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
