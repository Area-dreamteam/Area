import 'package:flutter/material.dart';
import 'package:mobile/services/api_service.dart';
import 'package:mobile/repositories/auth_repository.dart';
import 'package:mobile/viewmodels/register_viewmodel.dart';
import 'package:mobile/viewmodels/login_viewmodel.dart';
import 'package:provider/provider.dart';
import 'package:mobile/scaffolds/main_scaffold.dart';
import 'package:mobile/repositories/service_repository.dart';
import 'package:mobile/viewmodels/create_viewmodel.dart';
import 'package:mobile/viewmodels/select_service_viewmodel.dart';
import 'package:mobile/viewmodels/my_applet_viewmodel.dart';
import 'package:mobile/viewmodels/explore_viewmodel.dart';
import 'package:mobile/viewmodels/profile_viewmodel.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  final apiService = ApiService();
  final authRepository = AuthRepository(apiService: apiService);
  final servicesRepository = ServiceRepository(apiService: apiService);

  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(
          create: (_) => LoginViewModel(authRepository: authRepository),
        ),
        ChangeNotifierProvider(
          create: (_) => RegisterViewModel(authRepository: authRepository),
        ),
        ChangeNotifierProvider(
          create: (_) =>
              MyAppletViewModel(serviceRepository: servicesRepository),
        ),
        ChangeNotifierProvider(
          create: (_) => CreateViewModel(serviceRepository: servicesRepository),
        ),
        ChangeNotifierProvider(
          create: (_) =>
              SelectServiceViewmodel(serviceRepository: servicesRepository),
        ),
        ChangeNotifierProvider(
          create: (_) =>
              ExploreViewModel(serviceRepository: servicesRepository)
                ..fetchExploreItems(),
        ),
        ChangeNotifierProvider(
          create: (_) =>
              ProfileViewModel(serviceRepository: servicesRepository),
        ),
        Provider.value(value: authRepository),
        Provider.value(value: apiService),
        Provider.value(value: servicesRepository),
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AREA',
      home: const MainPage(),
      debugShowCheckedModeBanner: false,
    );
  }
}
