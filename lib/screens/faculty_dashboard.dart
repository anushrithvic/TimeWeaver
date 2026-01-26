import 'package:flutter/material.dart';

class FacultyDashboard extends StatelessWidget {
  const FacultyDashboard({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Faculty Timetable'),
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: 5,
        itemBuilder: (context, index) {
          return Card(
            child: ListTile(
              leading: const Icon(Icons.class_),
              title: Text('Course ${index + 1}'),
              subtitle: const Text('Mon • 10:00 AM – 11:00 AM'),
            ),
          );
        },
      ),
    );
  }
}