#include <iostream>
#include <mongocxx/client.hpp>
#include <mongocxx/cursor.hpp>
#include <mongocxx/exception/exception.hpp>

void run(){
  mongocxx::client conn{mongocxx::uri{}};
  auto cursor = conn.list_databases();
  std::cout << "Listing Databases: " << std::endl;
  for (auto&& x : cursor) {
    std::cout << x["name"].get_utf8().value << std::endl;
  }
}

int main(int, char**) {
    try{
      run();
      std::cout << "connected ok" << std::endl;
    } catch( const mongocxx::exception &e ) {
      std::cout << "caught " << e.what() << std::endl;
    }
    return EXIT_SUCCESS;

}
