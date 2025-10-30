import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:mobile/viewmodels/explore_viewmodel.dart';
import 'package:mobile/models/service_model.dart';
import 'package:mobile/widgets/card.dart';
import 'package:mobile/widgets/service_card.dart';
import 'package:mobile/widgets/navbar.dart';
import 'package:mobile/pages/information_page.dart';

class ExplorePage extends StatefulWidget {
  const ExplorePage({super.key});

  @override
  State<ExplorePage> createState() => _ExplorePageState();
}

class _ExplorePageState extends State<ExplorePage> {
  final TextEditingController _searchCtrl = TextEditingController();
  String _selectedCategory = 'All';

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<ExploreViewModel>().fetchExploreItems();
    });
    _searchCtrl.addListener(() => setState(() {}));
  }

  List<ExploreItem> get _filteredItems {
    final viewModel = context.read<ExploreViewModel>();
    final searchText = _searchCtrl.text.trim().toLowerCase();

    return viewModel.allItems.where((item) {
      final matchesCategory =
          _selectedCategory == 'All' || item.type == _selectedCategory;
      final matchesQuery =
          searchText.isEmpty || item.title.toLowerCase().contains(searchText);
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
    return Scaffold(
      backgroundColor: const Color(0xFF212121),
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
                prefixIcon: const Icon(Icons.search, color: Colors.grey),
                filled: true,
                fillColor: Colors.white,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
              ),
              style: const TextStyle(color: Colors.black),
            ),
            const SizedBox(height: 12),
            Expanded(
              child: Consumer<ExploreViewModel>(
                builder: (context, viewModel, child) {
                  if (viewModel.isLoading) {
                    return const Center(child: CircularProgressIndicator());
                  }
                  final items = _filteredItems;
                  return ListView.builder(
                    itemCount: items.length,
                    itemBuilder: (context, index) {
                      final item = items[index];

                      if (item.type == 'Applet') {
                        return Padding(
                          padding: const EdgeInsets.symmetric(vertical: 8.0),
                          child: AppletCard(
                            colorHex: item.colorHex,
                            title: item.title,
                            byText: item.byText ?? 'By Unknown',
                            onTap: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (context) =>
                                      InformationPage(item: item),
                                ),
                              );
                            },
                          ),
                        );
                      } else {
                        final serviceData = item.data as Service;
                        return Padding(
                          padding: const EdgeInsets.symmetric(vertical: 8.0),
                          child: ServiceCard(
                            id: serviceData.id,
                            name: serviceData.name,
                            colorHex: serviceData.color,
                            imageUrl: serviceData.imageUrl,
                            onTap: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (context) =>
                                      InformationPage(item: item),
                                ),
                              );
                            },
                          ),
                        );
                      }
                    },
                  );
                },
              ),
            ),
          ],
        ),
      ),
      bottomNavigationBar: const MyBottomNavigationBar(selectedIndex: 1),
    );
  }
}