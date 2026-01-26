import 'package:flutter/material.dart';

void main() {
  runApp(const TimeWeaverApp());
}

class TimeWeaverApp extends StatelessWidget {
  const TimeWeaverApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'TimeWeaver Admin',
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF6366F1), // Indigo primary
          background: const Color(0xFFF8FAFC),
        ),
      ),
      home: const MainAdminShell(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class MainAdminShell extends StatefulWidget {
  const MainAdminShell({super.key});

  @override
  State<MainAdminShell> createState() => _MainAdminShellState();
}

class _MainAdminShellState extends State<MainAdminShell> {
  int _selectedIndex = 0;

  final List<Widget> _screens = [
    const DashboardOverview(),
    const FacultyManager(),
    const TimetableGenerator(),
  ];

  @override
  Widget build(BuildContext context) {
    bool isWide = MediaQuery.of(context).size.width > 1000;

    return Scaffold(
      body: Row(
        children: [
          NavigationRail(
            extended: isWide,
            selectedIndex: _selectedIndex,
            onDestinationSelected: (int index) => setState(() => _selectedIndex = index),
            leading: const Padding(
              padding: EdgeInsets.symmetric(vertical: 24),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.auto_awesome, color: Color(0xFF6366F1), size: 32),
                  SizedBox(width: 8),
                  Text("TimeWeaver", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
                ],
              ),
            ),
            destinations: const [
              NavigationRailDestination(
                icon: Icon(Icons.dashboard_outlined),
                selectedIcon: Icon(Icons.dashboard),
                label: Text('Overview'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.people_outline),
                selectedIcon: Icon(Icons.people),
                label: Text('Faculty Workload'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.grid_on_outlined),
                selectedIcon: Icon(Icons.grid_on),
                label: Text('Master Timetable'),
              ),
            ],
          ),
          const VerticalDivider(thickness: 1, width: 1),
          Expanded(child: _screens[_selectedIndex]),
        ],
      ),
    );
  }
}

// --- 1. DASHBOARD OVERVIEW ---
class DashboardOverview extends StatelessWidget {
  const DashboardOverview({super.key});

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(32.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text("System Overview", style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
          const SizedBox(height: 24),
          Row(
            children: [
              _statCard("Total Faculty", "124", Colors.blue, Icons.person),
              _statCard("Total Sections", "32", Colors.orange, Icons.groups),
              _statCard("Room Utilization", "82%", Colors.green, Icons.room),
              _statCard("Pending Conflicts", "0", Colors.red, Icons.warning_amber),
            ],
          ),
          const SizedBox(height: 32),
          const Text("Quick Actions", style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          const SizedBox(height: 16),
          Wrap(
            spacing: 16,
            children: [
              _actionButton("Upload Faculty CSV", Icons.upload_file),
              _actionButton("Configure Room Labs", Icons.settings_input_component),
              _actionButton("System Logs", Icons.history),
            ],
          ),
        ],
      ),
    );
  }

  Widget _statCard(String label, String value, Color color, IconData icon) {
    return Expanded(
      child: Card(
        elevation: 0,
        shape: RoundedRectangleBorder(side: BorderSide(color: Colors.grey.shade200), borderRadius: BorderRadius.circular(16)),
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Icon(icon, color: color, size: 28),
              const SizedBox(height: 16),
              Text(label, style: const TextStyle(color: Colors.grey, fontSize: 14)),
              Text(value, style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
            ],
          ),
        ),
      ),
    );
  }

  Widget _actionButton(String label, IconData icon) {
    return OutlinedButton.icon(
      style: OutlinedButton.styleFrom(padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 20)),
      onPressed: () {},
      icon: Icon(icon),
      label: Text(label),
    );
  }
}

// --- 2. FACULTY MANAGER ---
class FacultyManager extends StatelessWidget {
  const FacultyManager({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(32.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text("Workload Distribution", style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
              FilledButton.icon(onPressed: () {}, icon: const Icon(Icons.person_add), label: const Text("Add Faculty")),
            ],
          ),
          const SizedBox(height: 24),
          Expanded(
            child: Card(
              elevation: 0,
              shape: RoundedRectangleBorder(side: BorderSide(color: Colors.grey.shade200)),
              child: ListView(
                children: [
                  _facultyItem("Dr. Sarah Thorne", "Computer Science", 16, 18),
                  _facultyItem("Prof. Alan Turing", "Mathematics", 12, 15),
                  _facultyItem("Dr. Grace Hopper", "Information Tech", 20, 18), // Example of overload
                  _facultyItem("James Gosling", "Software Engineering", 8, 18),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _facultyItem(String name, String dept, int current, int max) {
    double progress = current / max;
    bool isOverloaded = current > max;
    return ListTile(
      contentPadding: const EdgeInsets.all(16),
      leading: CircleAvatar(backgroundColor: Colors.indigo.shade100, child: Text(name[0])),
      title: Text(name, style: const TextStyle(fontWeight: FontWeight.bold)),
      subtitle: Text(dept),
      trailing: SizedBox(
        width: 300,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            Text("$current / $max Hours", style: TextStyle(fontWeight: FontWeight.bold, color: isOverloaded ? Colors.red : Colors.green)),
            const SizedBox(height: 8),
            LinearProgressIndicator(
              value: progress > 1 ? 1 : progress,
              color: isOverloaded ? Colors.red : Colors.indigo,
              backgroundColor: Colors.grey.shade200,
            ),
          ],
        ),
      ),
    );
  }
}

// --- 3. MASTER TIMETABLE ENGINE ---
class TimetableGenerator extends StatefulWidget {
  const TimetableGenerator({super.key});

  @override
  State<TimetableGenerator> createState() => _TimetableGeneratorState();
}

class _TimetableGeneratorState extends State<TimetableGenerator> {
  String selectedDept = 'Computer Science';
  String selectedYear = '3rd Year';
  String selectedSection = 'Section A';

  @override
  Widget build(BuildContext context) {
    final days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];
    final times = ['09:00', '10:00', '11:00', '12:00', '01:00', '02:00', '03:00'];

    return Padding(
      padding: const EdgeInsets.all(32.0),
      child: Column(
        children: [
          Row(
            children: [
              const Text("Master Schedule", style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
              const Spacer(),
              _filterDropdown("Dept", selectedDept, ['Computer Science', 'Electrical', 'Civil'], (val) => setState(() => selectedDept = val!)),
              const SizedBox(width: 12),
              _filterDropdown("Year", selectedYear, ['1st Year', '2nd Year', '3rd Year', '4th Year'], (val) => setState(() => selectedYear = val!)),
              const SizedBox(width: 12),
              _filterDropdown("Section", selectedSection, ['Section A', 'Section B', 'Section C'], (val) => setState(() => selectedSection = val!)),
            ],
          ),
          const SizedBox(height: 24),
          Expanded(
            child: Container(
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: Colors.grey.shade200),
              ),
              child: ClipRRect(
                borderRadius: BorderRadius.circular(16),
                child: SingleChildScrollView(
                  child: Table(
                    columnWidths: const {0: FixedColumnWidth(100)},
                    border: TableBorder.all(color: Colors.grey.shade100, width: 1),
                    children: [
                      TableRow(
                        decoration: BoxDecoration(color: Colors.grey.shade50),
                        children: [
                          const _HeaderCell("Time"),
                          ...days.map((d) => _HeaderCell(d)).toList(),
                        ],
                      ),
                      ...times.map((time) => TableRow(
                        children: [
                          Padding(padding: const EdgeInsets.all(20), child: Center(child: Text(time, style: const TextStyle(color: Colors.grey)))),
                          ...days.map((day) => _ScheduleCell(day, time)).toList(),
                        ],
                      )).toList(),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _filterDropdown(String label, String value, List<String> items, ValueChanged<String?> onChanged) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
      decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(8), border: Border.all(color: Colors.grey.shade300)),
      child: DropdownButton<String>(
        value: value,
        underline: const SizedBox(),
        items: items.map((e) => DropdownMenuItem(value: e, child: Text(e, style: const TextStyle(fontSize: 13)))).toList(),
        onChanged: onChanged,
      ),
    );
  }
}

class _HeaderCell extends StatelessWidget {
  final String title;
  const _HeaderCell(this.title);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 20),
      child: Center(child: Text(title, style: const TextStyle(fontWeight: FontWeight.bold))),
    );
  }
}

class _ScheduleCell extends StatelessWidget {
  final String day;
  final String time;
  const _ScheduleCell(this.day, this.time);

  @override
  Widget build(BuildContext context) {
    // Logic to mock an occupied slot
    bool isOccupied = (day == 'Mon' && time == '09:00') || (day == 'Wed' && time == '11:00') || (day == 'Fri' && time == '02:00');

    return Container(
      height: 120,
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: isOccupied ? const Color(0xFF6366F1).withOpacity(0.05) : Colors.transparent,
      ),
      child: isOccupied 
        ? Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(color: const Color(0xFF6366F1), borderRadius: BorderRadius.circular(4)),
                child: const Text("CS301: AI", style: TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold)),
              ),
              const SizedBox(height: 8),
              const Text("Dr. Sarah Thorne", style: TextStyle(fontSize: 11, fontWeight: FontWeight.w600)),
              const Spacer(),
              const Row(
                children: [
                  Icon(Icons.location_on_outlined, size: 12, color: Colors.grey),
                  SizedBox(width: 4),
                  Text("Lab 201", style: TextStyle(fontSize: 10, color: Colors.grey)),
                ],
              )
            ],
          )
        : const SizedBox(),
    );
  }
}