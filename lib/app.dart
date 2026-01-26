import 'package:flutter/material.dart';
import 'screens/admin_dashboard.dart';
import 'theme/app_theme.dart';

class TimeWeaverApp extends StatelessWidget {
  const TimeWeaverApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'TimeWeaver',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      home: const AdminDashboard(),
    );
  }
}