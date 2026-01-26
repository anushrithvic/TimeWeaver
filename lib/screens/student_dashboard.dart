import 'package:flutter/material.dart';

class StudentDashboard extends StatelessWidget {
  const StudentDashboard({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Student Timetable')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: const [
            Icon(Icons.schedule, size: 80, color: Colors.indigo),
            SizedBox(height: 16),
            Text(
              'Search your timetable by class or section',
              style: TextStyle(fontSize: 16),
            ),
          ],
        ),
      ),
    );
  }
}