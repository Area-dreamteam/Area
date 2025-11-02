// Import all test files
import 'models/action_model_test.dart' as action_model_test;
import 'models/reaction_model_test.dart' as reaction_model_test;
import 'models/applet_model_test.dart' as applet_model_test;
import 'models/user_model_test.dart' as user_model_test;
import 'models/service_model_test.dart' as service_model_test;
import 'models/service_info_model_test.dart' as service_info_model_test;
import 'widgets/hex_convert_test.dart' as hex_convert_test;
import 'widgets/widgets_test.dart' as widgets_test;
import 'viewmodels/login_viewmodel_test.dart' as login_viewmodel_test;
import 'viewmodels/register_viewmodel_test.dart' as register_viewmodel_test;
import 'viewmodels/my_applet_viewmodel_test.dart' as my_applet_viewmodel_test;
import 'viewmodels/change_password_viewmodel_test.dart' as change_password_viewmodel_test;
import 'viewmodels/profile_viewmodel_test.dart' as profile_viewmodel_test;
import 'viewmodels/explore_viewmodel_test.dart' as explore_viewmodel_test;
import 'viewmodels/select_service_viewmodel_test.dart' as select_service_viewmodel_test;
import 'viewmodels/create_viewmodel_test.dart' as create_viewmodel_test;
import 'services/api_url_service_test.dart' as api_url_service_test;
import 'core/config_test.dart' as config_test;

void main() {
  action_model_test.main();
  reaction_model_test.main();
  applet_model_test.main();
  user_model_test.main();
  service_model_test.main();
  service_info_model_test.main();
  hex_convert_test.main();
  widgets_test.main();
  login_viewmodel_test.main();
  register_viewmodel_test.main();
  my_applet_viewmodel_test.main();
  change_password_viewmodel_test.main();
  profile_viewmodel_test.main();
  explore_viewmodel_test.main();
  select_service_viewmodel_test.main();
  create_viewmodel_test.main();
  api_url_service_test.main();
  config_test.main();
}