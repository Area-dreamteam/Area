import { Column, Entity, ObjectIdColumn, PrimaryGeneratedColumn, CreateDateColumn, UpdateDateColumn } from 'typeorm';
import { Role } from '../common/enum/role.enum'


@Entity('users')
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ unique: true })
  username: string;
  
  @Column({unique: true})
  email: string;
  
  @Column()
  password: string;
  
  @Column({ default: 'user' })
  role: Role;

  @CreateDateColumn()
  createdAt: Date;
  
  @UpdateDateColumn()
  updatedAt: Date;
}
