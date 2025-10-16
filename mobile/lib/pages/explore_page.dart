/*import 'package:flutter/material.dart';
//import '../widgets/card.dart';
import '../widgets/service_card.dart';
import '../widgets/navbar.dart';

class ExplorePage extends StatefulWidget {
  const ExplorePage({super.key});

  @override
  State<ExplorePage> createState() => _ExplorePageState();
}

class _ExplorePageState extends State<ExplorePage> {
  final TextEditingController _searchCtrl = TextEditingController();

  final List<Map<String, String>> _allItems = [
    {
      'title': 'Super Applet',
      'type': 'Applet',
      'by': 'IFTTT',
      'users': '12k',
      'color': '0xFFE86E66',
    },
    {
      'title': 'Weather Service',
      'type': 'Service',
      'by': 'Community',
      'users': '8k',
      'color': '0xFF2B2140',
    },
    {
      'title': 'Smart Home Applet',
      'type': 'Applet',
      'by': 'IFTTT',
      'users': '20k',
      'color': '0xFFE86E66',
    },
  ];

  String _selectedCategory = 'All';

  List<Map<String, String>> get _filteredItems {
    final searchText = _searchCtrl.text.trim().toLowerCase();
    return _allItems.where((word) {
      final matchesCategory =
          _selectedCategory == 'All' || word['type'] == _selectedCategory;
      final matchesQuery =
          searchText.isEmpty ||
          word['title']!.toLowerCase().contains(searchText);
      return matchesCategory && matchesQuery;
    }).toList();
  }

  Widget _buildCategoryButtons() {
    final categories = ['All', 'Applet', 'Service'];
    return Row(
      children: categories.map((tab) {
        final selected = tab == _selectedCategory;
        return Expanded(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 4.0),
            child: ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: selected ? Colors.blue : Colors.grey.shade200,
                foregroundColor: selected ? Colors.white : Colors.black,
                padding: const EdgeInsets.symmetric(vertical: 14),
              ),
              onPressed: () {
                setState(() => _selectedCategory = tab);
              },
              child: Text(tab),
            ),
          ),
        );
      }).toList(),
    );
  }

  @override
  void dispose() {
    _searchCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final items = _filteredItems;

    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(12.0),
        child: Column(
          children: [
            const SizedBox(height: 60),
            _buildCategoryButtons(),
            const SizedBox(height: 20),

            TextField(
              controller: _searchCtrl,
              onChanged: (_) => setState(() {}),
              decoration: InputDecoration(
                hintText: 'Search',
                prefixIcon: const Icon(Icons.search),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
              ),
            ),
            const SizedBox(height: 12),

            Expanded(
              child: GridView.builder(
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2,
                  mainAxisSpacing: 12,
                  crossAxisSpacing: 12,
                  childAspectRatio: 0.70,
                ),
                itemCount: items.length,
                itemBuilder: (context, index) {
                  final item = items[index];
                  final color = int.parse(item['color']!);
             //     final type = item['type'];

        //          if (type == 'Applet') {
           //         return BigCard(
             //         color: Color(color),
               //       icon: Icons.extension,
         //             title: item['title']!,
       //               byText: item['by']!,
          //            onTap: () {},
          //          );
            //      } else {
  //                  return ServiceCard(
    //                  color: Color(color),
      ///                icon: Icons.cloud,
         ///             title: item['title']!,
            //          onTap: () {},
    //                );
                  }
 //               },
              ),
            ),
          ],
        ),
      ),
      bottomNavigationBar: const MyBottomNavigationBar(selectedIndex: 1),
    );
  }
}
*/