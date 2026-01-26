import 'package:flutter/material.dart';
import '../widgets/timetable_card.dart';
import '../widgets/workload_chart.dart';

class AdminDashboard extends StatelessWidget {
  const AdminDashboard({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('TimeWeaver – Admin Dashboard'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: GridView.count(
          crossAxisCount: 2,
          crossAxisSpacing: 16,
          mainAxisSpacing: 16,
          children: const [
            TimetableCard(
              title: 'Generate Timetable',
              icon: Icons.calendar_month,
            ),
            TimetableCard(
              title: 'Faculty Workload',
              icon: Icons.people,
            ),
            TimetableCard(
              title: 'Room Utilization',
              icon: Icons.meeting_room,
            ),
            TimetableCard(
              title: 'Scenario Simulation',
              icon: Icons.auto_graph,
            ),
            WorkloadChart(),
          ],
        ),
      ),
    );
  }
}