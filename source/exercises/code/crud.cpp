#include <iostream>
#include <mongocxx/client.hpp>
#include <mongocxx/cursor.hpp>
#include <mongocxx/collection.hpp>
#include <bsoncxx/builder/stream/document.hpp>
#include <bsoncxx/builder/basic/kvp.hpp>
#include <mongocxx/exception/exception.hpp>

using namespace bsoncxx::builder::stream;
using namespace mongocxx;

using bsoncxx::builder::basic::kvp;

void insert(){
  // instantiate a connection
  client conn{mongocxx::uri{}};
  //instantiate a collection
  collection coll = conn["sample"]["cpp"];
  //create a document
  auto doc0 = document{} << "name" << "Dwight" << finalize;

  //insert the document
  coll.insert_one(doc0.view());
}

void insert_with_id(){
  // instantiate a connection
  client conn{mongocxx::uri{}};
  //instantiate a collection
  collection coll = conn["sample"]["cpp"];

  //create a document
  auto doc1 = document{} << "_id" << 1 << "name" << "Dwight" << finalize;

  //insert the document
  coll.insert_one(doc1.view());
  //
  auto cursor = coll.find({});
  for (auto&& x : cursor) {
    std::cout << "_id: " << x["_id"].get_int32() << std::endl;
  }
}


void insert__id_array(){
  // instantiate a connection
  client conn{mongocxx::uri{}};
  //instantiate a collection
  collection coll = conn["sample"]["cpp"];

  int a[3] = {0,1,2};
  //initialize a document
  auto doc2 = document{} << "_id" << open_array << 0 << 1 << 2<< close_array<< finalize;

  //insert a document
  coll.insert_one(doc2.view());

}

int main(int, char**) {
    try{
      insert__id_array();
    } catch( const exception &e ) {
      std::cout << "caught " << e.what() << std::endl;
    }
    return EXIT_SUCCESS;

}
