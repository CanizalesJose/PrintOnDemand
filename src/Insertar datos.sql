use PrintOnDemand;

call registrarModelo("model1", "ArticulatedWhaleShark", "https://cdn.thingiverse.com/assets/d9/91/d7/44/d5/large_display_5939294b-57ab-4709-a2e5-3182f29fa89e.png", "ArticulatedWhaleShark.stl", 10.99);
call registrarModelo('model2', 'Cabinet Door Organizer', 'https://cdn.thingiverse.com/assets/8a/96/8b/7a/3b/large_display_707af456-9de0-4a2c-9e8a-1e7780eeef75.png', 'Cabinet_Door_Organizer_5.stl', 12.99);
call registrarModelo('model3', 'Anatomically Correct Human Skull (Homo Sapiens Sapiens)', 'https://cdn.thingiverse.com/assets/9a/e4/cd/5f/dc/large_display_f6557724-0b6c-4cea-bdc1-067a0a5194b9.png', 'Human_Skull_Cut_OBJ_3Demon.obj', 8.99);
call registrarModelo('model4', '8geo 3d', 'https://cdn.thingiverse.com/assets/fc/6c/80/e8/46/large_display_40278189-9e71-41eb-9750-6e92d2331aff.png', 'x8geo_3d_planter.stl', 15.99);
call registrarModelo('model5', 'Articulated Dolphin', 'https://cdn.thingiverse.com/assets/b5/be/1b/af/71/large_display_89e2f9a3-7290-4152-a174-e8b640d77a84.png', 'Extreemly_loose_dolphin_rec.stl', 9.99);
call registrarModelo('model6', 'Vox\'s hat', 'https://cdn.thingiverse.com/assets/cb/3c/26/7e/54/large_display_7675b91a-d933-479b-8cb2-4b9b0b31b4af.png', 'tv_hat.stl', 11.99);
call registrarModelo('model7', 'Saturn V - Desktop Rocket', 'https://cdn.thingiverse.com/assets/4e/bf/63/63/42/large_display_8dc51bee-8a08-4b59-a034-71129db06b65.png', 'Saturn_V_Desktop_-_Rocket.stl', 14.99);
call registrarModelo('model8', 'A-10 Warthog', 'https://cdn.thingiverse.com/assets/f5/71/5c/fc/64/large_display_0339506b-8ccc-429b-8ea7-64aef7bedbdc.png', 'A-10_Warthog.stl', 13.99);
call registrarModelo('model9', 'Window for Dollhouse', 'https://cdn.thingiverse.com/assets/f4/69/fb/f5/de/large_display_0c2a8d5f-e793-43c6-ab9b-f8436656e649.png', 'Part_Studio_1.stl', 7.99);
call registrarModelo('model10', 'Rejilla ventilador', 'https://cdn.thingiverse.com/assets/67/c9/2a/2c/6c/large_display_8c03cb80-8a62-4c27-b35e-9e7d5ac9470d.png', 'rejilla_vent2.stl', 16.9);

INSERT INTO userTypes VALUES (1, "Administrador"), (2, "Usuario Cliente");

call registrarUser("admin", "123", 1);
call registrarUser("client", "123", 2);

call registrarMaterial("material1", "PLA", 1);
call registrarMaterial("material2", "ABS", 1.2);
call registrarMaterial("material3", "PETG", 1.1);
call registrarMaterial("material4", "TPU", 1.3);

call registrarValidMaterial("model1", "material1");
call registrarValidMaterial("model1", "material2");
call registrarValidMaterial("model1", "material3");
call registrarValidMaterial("model1", "material4");

call registrarValidMaterial("model2", "material1");
call registrarValidMaterial("model2", "material2");
call registrarValidMaterial("model2", "material4");

call registrarValidMaterial("model3", "material1");
call registrarValidMaterial("model3", "material4");

call registrarValidMaterial("model4", "material1");
call registrarValidMaterial("model4", "material3");

call registrarValidMaterial("model5", "material1");

call registrarValidMaterial("model6", "material2");

select * from validmaterials;

delete from validmaterials where modelkey = "model6" and materialKey = "material2";
