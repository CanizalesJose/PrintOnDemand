use PrintOnDemand;

INSERT INTO models3D (modelId, modelName, modelImage, modelFile, modelBasePrice)
VALUES
    ('model1', 'Modelo 1', 'url_imagen_1.jpg', 'modelo1.stl', 10.99),
    ('model2', 'Modelo 2', 'url_imagen_2.jpg', 'modelo2.stl', 12.99),
    ('model3', 'Modelo 3', 'url_imagen_3.jpg', 'modelo3.stl', 8.99),
    ('model4', 'Modelo 4', 'url_imagen_4.jpg', 'modelo4.stl', 15.99),
    ('model5', 'Modelo 5', 'url_imagen_5.jpg', 'modelo5.stl', 9.99),
    ('model6', 'Modelo 6', 'url_imagen_6.jpg', 'modelo6.stl', 11.99),
    ('model7', 'Modelo 7', 'url_imagen_7.jpg', 'modelo7.stl', 14.99),
    ('model8', 'Modelo 8', 'url_imagen_8.jpg', 'modelo8.stl', 13.99),
    ('model9', 'Modelo 9', 'url_imagen_9.jpg', 'modelo9.stl', 7.99),
    ('model10', 'Modelo 10', 'url_imagen_10.jpg', 'modelo10.stl', 16.99
);

SELECT * FROM models3D;

INSERT INTO userTypes VALUES (1, "admin"), (2, "cliente");

SELECT * FROM userTypes;

call registrarUser("pablo", "123", 1);
call registrarUser("pablopobre", "123", 2);

SELECT * FROM users;