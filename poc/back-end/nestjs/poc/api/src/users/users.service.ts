import { Injectable, UnauthorizedException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { hash } from 'bcrypt';
import { User } from './user.entity';
import { DataSource } from 'typeorm';
import { Role } from 'src/common/enum/role.enum';

@Injectable()
export class UsersService {
  constructor(
    @InjectRepository(User)
    private readonly usersRepo: Repository<User>,
    private readonly dataSource: DataSource
  ) {}

  async create(email: string, username: string, password: string, role: Role = Role.User): Promise<User> {
    const hashedPassword = await hash(password, 10);
    const user = this.usersRepo.create({ email, username, password: hashedPassword, role });
    return this.usersRepo.save(user);
  }

  async findByEmail(email: string): Promise<User | null> {
    return this.usersRepo.findOne({ where: { email } });
  }

  async findById(id: number): Promise<User | null> {
    return this.usersRepo.findOne({ where: { id } });
  }

  async update(id: number, fields: Partial<User>): Promise<User> {
    const user = await this.findById(id);
    if (!user)
      throw new Error('User not found');

    if (fields.password)
      fields.password = await hash(fields.password, 10);

    Object.assign(user, fields);
    return this.usersRepo.save(user);
  }
}

