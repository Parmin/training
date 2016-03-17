#include <algorithm>
#include <iostream>
#include <iterator>
#include <vector>

#include <bsoncxx/array/view.hpp>
#include <bsoncxx/array/view.hpp>
#include <bsoncxx/builder/basic/array.hpp>
#include <bsoncxx/builder/basic/document.hpp>
#include <bsoncxx/builder/basic/kvp.hpp>
#include <bsoncxx/document/value.hpp>
#include <bsoncxx/document/view.hpp>
#include <bsoncxx/json.hpp>
#include <bsoncxx/stdx/string_view.hpp>
#include <bsoncxx/types.hpp>
#include <bsoncxx/types/value.hpp>

#include <mongocxx/exception/exception.hpp>
#include <mongocxx/collection.hpp>
#include <mongocxx/client.hpp>
#include <mongocxx/cursor.hpp>

using namespace bsoncxx;
using namespace mongocxx;

void array_operators() {
  // basic builder
  using namespace builder::basic;

  builder::basic::document query;
  query.append(kvp("category", [](sub_document sd) {
                sd.append(kvp("$all",[](sub_array sa) {
                  sa.append("sci-fi", "action"); }));}
              ));

  query.append(kvp("category", [](sub_document sd) {
                sd.append(kvp("$size", 1));}));
}

void element_operators(){
  // instantiate a connection
  client conn{mongocxx::uri{}};
  // instantiate a collection
  collection coll = conn["sample"]["movies"];

  // basic builder
  using namespace builder::basic;

  builder::basic::document query;
  query.append(kvp("budget", [](sub_document sd) {
                sd.append(kvp("$type", 1));}));


  coll.find(query.view());

}


int main(int, char**) {
    try{
      element_operators();
    } catch( const exception &e ) {
      std::cout << "caught " << e.what() << std::endl;
    }
    return EXIT_SUCCESS;

}
