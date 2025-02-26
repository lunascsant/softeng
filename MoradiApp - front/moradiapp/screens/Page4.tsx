import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { MaterialIcons } from 'react-native-vector-icons';
import { useNavigation } from '@react-navigation/native';

export default function HomeScreen() {
  const navigation = useNavigation(); // Hook de navegação

  return (
    <View style={styles.container}>
      <Text style={styles.subtitle}>Suas Repúblicas</Text>

      <ScrollView style={styles.listContainer}>
        {/* Moradia 01 */}
        <View style={styles.moradiaCard}>
          <View style={styles.cardHeader}>
            <MaterialIcons name="home" size={30} color="#F5A623" />
            <Text style={styles.moradiaTitle}>Moradia 01</Text>
          </View>
          <Text style={styles.cardText}>Grupo: Luciana, Carolina, Duda... ver mais</Text>
          <Text style={styles.cardText}>Endereço: Rua Adolpho Kirchmaeir</Text>
        </View>

        {/* Moradia 02 (Navegação para a página 5) */}
        <TouchableOpacity
          style={styles.moradiaCard}
          onPress={() => navigation.navigate('Page5')} // Navegação para a Página 5
        >
          <View style={styles.cardHeader}>
            <MaterialIcons name="home" size={30} color="#F5A623" />
            <Text style={styles.moradiaTitle}>Moradia 02</Text>
          </View>
          <Text style={styles.cardText}>Grupo: Manoela, Nair, Julia Heloiza ... ver mais</Text>
          <Text style={styles.cardText}>Endereço: Rua Prefeito Sebastião</Text>
        </TouchableOpacity>

        {/* Moradia 03 */}
        <View style={styles.moradiaCard}>
          <View style={styles.cardHeader}>
            <MaterialIcons name="home" size={30} color="#F5A623" />
            <Text style={styles.moradiaTitle}>Moradia 03</Text>
          </View>
          <Text style={styles.cardText}>Grupo: Lucas, João, Tiago... ver mais</Text>
          <Text style={styles.cardText}>Endereço: Rua José Lourenço</Text>
        </View>
      </ScrollView>

      <TouchableOpacity style={styles.createGroupButton}>
        <Text style={styles.createGroupButtonText}>Criar novo grupo</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F2F6F7',
    paddingHorizontal: 20,
    paddingTop: 40,
  },
  subtitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2C3E50',
    marginBottom: 20,
  },
  listContainer: {
    flex: 1,
  },
  moradiaCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 10,
    padding: 15,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 5,
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  moradiaTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginLeft: 10,
    color: '#2C3E50',
  },
  cardText: {
    fontSize: 14,
    color: '#7F8C8D',
    marginBottom: 5,
  },
  createGroupButton: {
    backgroundColor: '#2C3E50',
    borderRadius: 25,
    paddingVertical: 15,
    alignItems: 'center',
    marginTop: 20,
    marginBottom: 40,
  },
  createGroupButtonText: {
    fontSize: 18,
    color: '#FFFFFF',
    fontWeight: 'bold',
  },
});
