import 'package:flutter/material.dart';
import 'package:mobile/models/action_model.dart';
import 'package:mobile/models/reaction_model.dart';
import 'package:mobile/pages/choose_service_page.dart';
import 'package:mobile/viewmodels/create_viewmodel.dart';
import 'package:mobile/widgets/create_card.dart';
import 'package:mobile/widgets/navbar.dart';
import 'package:provider/provider.dart';
import 'package:mobile/pages/review_and_finish_page.dart';

class CreatePage extends StatefulWidget {
  const CreatePage({super.key});

  @override
  State<CreatePage> createState() => _CreatePageState();
}

class _CreatePageState extends State<CreatePage> {

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final viewModel = context.read<CreateViewModel>();
      if (!viewModel.isEditing) {
        viewModel.clearSelection();
      }
    });
  }

  @override
  void dispose() {
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF212121),
      body: Consumer<CreateViewModel>(
        builder: (context, viewModel, child) {
          return Center(
            child: SingleChildScrollView(
              padding: const EdgeInsets.symmetric(horizontal: 20.0),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  _header(),
                  const SizedBox(height: 40),
                  _ifThisCard(context, viewModel),
                  const SizedBox(height: 20),
                  const Icon(
                    Icons.arrow_downward,
                    color: Colors.white,
                    size: 30,
                  ),
                  const SizedBox(height: 20),
                  _thenThatCard(context, viewModel),
                  const SizedBox(height: 40),
                  _feedbackAndActionButton(context, viewModel),
                ],
              ),
            ),
          );
        },
      ),
      bottomNavigationBar: const MyBottomNavigationBar(selectedIndex: 2),
    );
  }

  Widget _header() {
    return const Text(
      'Create your AREA',
      textAlign: TextAlign.center,
      style: TextStyle(
        fontSize: 50,
        fontWeight: FontWeight.bold,
        color: Colors.white,
      ),
    );
  }

  Widget _ifThisCard(BuildContext context, CreateViewModel viewModel) {
    final selectedAction = viewModel.selectedAction;

    return CreateCard(
      title: 'If This',
      details: selectedAction != null
          ? CardDetails(
              serviceName: selectedAction.service.name,
              actionName: selectedAction.item.name,
              imageUrl: selectedAction.service.imageUrl,
            )
          : null,
      onTap: () async {
        final result = await Navigator.push<ConfiguredItem<dynamic>?>(
          context,
          MaterialPageRoute(
            builder: (context) => const ChooseServicePage(type: 'trigger'),
          ),
        );
        if (result != null && context.mounted) {
          context.read<CreateViewModel>().selectAction(
            result as ConfiguredItem<ActionModel>,
          );
        }
      },
    );
  }

  Widget _thenThatCard(BuildContext context, CreateViewModel viewModel) {
    final selectedReaction = viewModel.selectedReaction;

    return CreateCard(
      title: 'Then That',
      details: selectedReaction != null
          ? CardDetails(
              serviceName: selectedReaction.service.name,
              actionName: selectedReaction.item.name,
              imageUrl: selectedReaction.service.imageUrl,
            )
          : null,
      onTap: () async {
        final result = await Navigator.push<ConfiguredItem<dynamic>?>(
          context,
          MaterialPageRoute(
            builder: (context) => const ChooseServicePage(type: 'reaction'),
          ),
        );
        if (result != null && context.mounted) {
          context.read<CreateViewModel>().selectReaction(
            result as ConfiguredItem<Reaction>,
          );
        }
      },
    );
  }

  Widget _feedbackAndActionButton(
    BuildContext context,
    CreateViewModel viewModel,
  ) {
    final bool isReady = viewModel.isActionAndReactionSelected;

    return ElevatedButton(
      style: ElevatedButton.styleFrom(
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
        padding: const EdgeInsets.symmetric(vertical: 16),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(30.0),
        ),
      ),
      onPressed: isReady
          ? () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => const ReviewAndFinishPage(),
                ),
              );
            }
          : null,
      child: const Text('Continue', style: TextStyle(fontSize: 18)),
    );
  }
}