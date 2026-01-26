import 'package:flutter/material.dart';

class WorkloadChart extends StatelessWidget {
  const WorkloadChart({super.key});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: const [
            Icon(Icons.bar_chart, size: 50, color: Colors.indigo),
            SizedBox(height: 12),
            Text(
              'Faculty Workload Analytics',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 8),
            Text('Charts will be rendered here'),
          ],
        ),
      ),
    );
  }
}