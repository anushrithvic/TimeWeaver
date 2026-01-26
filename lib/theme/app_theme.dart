import 'package:flutter/material.dart';

class AppTheme {
  static ThemeData lightTheme = ThemeData(
    useMaterial3: false, // IMPORTANT

    primaryColor: Colors.indigo,

    scaffoldBackgroundColor: Colors.grey.shade100,

    appBarTheme: const AppBarTheme(
      centerTitle: true,
      backgroundColor: Colors.indigo,
      foregroundColor: Colors.white,
      elevation: 2,
    ),

    cardTheme: const CardThemeData(
      elevation: 3,
      margin: EdgeInsets.all(8),
    ),
  );
}