import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import HomeScreen from './screens/HomeScreen';
import Page1 from './screens/Page1'; 
import Page2 from './screens/Page2';
import Page3 from './screens/Page3';
import Page4 from './screens/Page4';
import Page5 from './screens/Page5';
import Page6 from './screens/Page6';
import Page7 from './screens/Page7';
import Page8 from './screens/Page8';
import Page9 from './screens/Page9';

export type RootStackParamList = {
  Home: undefined;
  Page1: undefined;
  Page2: undefined;
  Page3: undefined;
  Page4: undefined;
  Page5: undefined;
  Page6: undefined;
  Page7: undefined;
  Page8: undefined;
  Page9: undefined;
};


const Stack = createNativeStackNavigator<RootStackParamList>();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="Home" component={HomeScreen} options={{ title: '' }} />
        <Stack.Screen name="Page1" component={Page1} options={{ title: '' }} />
        <Stack.Screen name="Page2" component={Page2} options={{ title: '' }} />
        <Stack.Screen name="Page3" component={Page3} options={{ title: '' }} />
        <Stack.Screen name="Page4" component={Page4} options={{ title: 'Página Principal' }} />
        <Stack.Screen name="Page5" component={Page5} options={{ title: 'Moradia 02' }} />
        <Stack.Screen name="Page6" component={Page6} options={{ title: 'Página Principal' }} />
        <Stack.Screen name="Page7" component={Page7} options={{ title: 'Sua República' }} />
        <Stack.Screen name="Page8" component={Page8} options={{ title: 'Página 8' }} />
        <Stack.Screen name="Page9" component={Page9} options={{ title: 'Moradia 01' }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
