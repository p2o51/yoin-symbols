import 'package:flutter/material.dart';
import 'package:yoin_symbols/yoin_symbols.dart';

void main() => runApp(const GalleryApp());

class GalleryApp extends StatelessWidget {
  const GalleryApp({super.key});

  static const Color _seed = Color(0xFF006C4E);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Yoin Symbols',
      theme: ThemeData(colorSchemeSeed: _seed),
      darkTheme: ThemeData(colorSchemeSeed: _seed, brightness: Brightness.dark),
      home: const GalleryPage(),
    );
  }
}

class GalleryPage extends StatefulWidget {
  const GalleryPage({super.key});

  @override
  State<GalleryPage> createState() => _GalleryPageState();
}

class _GalleryPageState extends State<GalleryPage> {
  String _query = '';

  @override
  Widget build(BuildContext context) {
    final entries = YoinSymbols.all.entries
        .where((e) => e.key.contains(_query.trim().toLowerCase()))
        .toList();
    final labelStyle = Theme.of(context).textTheme.labelSmall;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Yoin Symbols'),
        bottom: PreferredSize(
          preferredSize: const Size.fromHeight(64),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 0, 16, 12),
            child: TextField(
              decoration: const InputDecoration(
                prefixIcon: Icon(YoinSymbols.search),
                hintText: 'Search',
                border: OutlineInputBorder(),
                isDense: true,
              ),
              onChanged: (value) => setState(() => _query = value),
            ),
          ),
        ),
      ),
      body: GridView.builder(
        padding: const EdgeInsets.all(12),
        gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
          maxCrossAxisExtent: 112,
          childAspectRatio: 0.9,
        ),
        itemCount: entries.length,
        itemBuilder: (context, index) {
          final entry = entries[index];
          return Tooltip(
            message: 'YoinSymbols.${_camel(entry.key)}',
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(entry.value, size: 32),
                const SizedBox(height: 8),
                Text(entry.key, style: labelStyle, textAlign: TextAlign.center),
              ],
            ),
          );
        },
      ),
    );
  }

  static String _camel(String name) {
    final parts = name.split('_');
    return parts.first +
        parts.skip(1).map((p) => p[0].toUpperCase() + p.substring(1)).join();
  }
}
