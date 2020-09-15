INSERT INTO category (title, description, is_positive)
VALUES
  ('Useless', 'Activities to avoid', FALSE),
  ('Desired', 'Targeted activities', TRUE),
  ('Useful',  'Have to do', TRUE);

INSERT INTO activity (title, score, category_id)
VALUES
  ('Open A Social Network', 4, 1),
  ('Learn some finnish', 4, 2),
  ('Organize shelves', 2, 3);