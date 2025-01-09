from utils import hdv, bind, cossim

man = hdv()
sex_swap = hdv()
royalty_swap = hdv()
child_swap = hdv()

woman = bind(man, sex_swap)
king = bind(man, royalty_swap)
queen = bind(woman, royalty_swap)
prince = bind(king, child_swap)
princess = bind(queen, child_swap)
girl = bind(princess, royalty_swap)
boy = bind(princess, royalty_swap)

print(cossim( man, bind(woman, sex_swap)))
print(cossim( woman, bind(queen, royalty_swap)))
print(cossim( man, bind(queen, sex_swap, royalty_swap)))
print(cossim( man, bind(princess, sex_swap, royalty_swap, child_swap) ))
print(cossim( princess, bind(woman, child_swap, royalty_swap) ))
